import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../providers/profile_provider.dart';

class ProfileScreen extends ConsumerStatefulWidget {
  const ProfileScreen({super.key});

  @override
  ConsumerState<ProfileScreen> createState() => _ProfileScreenState();
}

class _ProfileScreenState extends ConsumerState<ProfileScreen> {
  final _formKey = GlobalKey<FormState>();
  final _firstNameController = TextEditingController();
  final _lastNameController = TextEditingController();
  bool _isEditing = false;

  @override
  void initState() {
    super.initState();
    // Fetch profile on init
    Future.microtask(() => ref.read(profileProvider.notifier).fetchProfile());
  }

  @override
  void dispose() {
    _firstNameController.dispose();
    _lastNameController.dispose();
    super.dispose();
  }

  void _toggleEdit() {
    setState(() {
      _isEditing = !_isEditing;
      if (_isEditing) {
        final profile = ref.read(profileProvider).profile;
        _firstNameController.text = profile?.prenom ?? '';
        _lastNameController.text = profile?.nom ?? '';
      }
    });
  }

  Future<void> _handleUpdate() async {
    if (_formKey.currentState?.validate() ?? false) {
      await ref.read(profileProvider.notifier).updateProfile({
        'first_name': _firstNameController.text,
        'last_name': _lastNameController.text,
      });

      if (mounted) {
        final profileState = ref.read(profileProvider);
        if (profileState.error == null) {
          setState(() {
            _isEditing = false;
          });
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(content: Text('Profile updated successfully')),
          );
        } else {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text(profileState.error!)),
          );
        }
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final profileState = ref.watch(profileProvider);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Profile'),
        actions: [
          if (!_isEditing)
            IconButton(
              icon: const Icon(Icons.edit),
              onPressed: _toggleEdit,
            ),
        ],
      ),
      body: profileState.isLoading && profileState.profile == null
          ? const Center(child: CircularProgressIndicator())
          : profileState.profile == null
              ? const Center(child: Text('Failed to load profile'))
              : SingleChildScrollView(
                  padding: const EdgeInsets.all(16.0),
                  child: Form(
                    key: _formKey,
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.stretch,
                      children: [
                        // Profile avatar
                        Center(
                          child: CircleAvatar(
                            radius: 50,
                            child: Text(
                              '${profileState.profile!.prenom[0]}${profileState.profile!.nom[0]}',
                              style: const TextStyle(fontSize: 32),
                            ),
                          ),
                        ),
                        const SizedBox(height: 24),

                        // Email (read-only)
                        TextFormField(
                          initialValue: profileState.profile!.email,
                          decoration: const InputDecoration(
                            labelText: 'Email',
                            border: OutlineInputBorder(),
                            prefixIcon: Icon(Icons.email),
                          ),
                          enabled: false,
                        ),
                        const SizedBox(height: 16),

                        // First name
                        TextFormField(
                          controller:
                              _isEditing ? _firstNameController : null,
                          initialValue:
                              _isEditing ? null : profileState.profile!.prenom,
                          decoration: const InputDecoration(
                            labelText: 'First Name',
                            border: OutlineInputBorder(),
                            prefixIcon: Icon(Icons.person),
                          ),
                          enabled: _isEditing,
                          validator: (value) {
                            if (value == null || value.isEmpty) {
                              return 'Please enter your first name';
                            }
                            return null;
                          },
                        ),
                        const SizedBox(height: 16),

                        // Last name
                        TextFormField(
                          controller: _isEditing ? _lastNameController : null,
                          initialValue:
                              _isEditing ? null : profileState.profile!.nom,
                          decoration: const InputDecoration(
                            labelText: 'Last Name',
                            border: OutlineInputBorder(),
                            prefixIcon: Icon(Icons.person_outline),
                          ),
                          enabled: _isEditing,
                          validator: (value) {
                            if (value == null || value.isEmpty) {
                              return 'Please enter your last name';
                            }
                            return null;
                          },
                        ),
                        const SizedBox(height: 16),

                        // Address (read-only for now)
                        TextFormField(
                          initialValue:
                              '${profileState.profile!.rue}, ${profileState.profile!.npa} ${profileState.profile!.localite}',
                          decoration: const InputDecoration(
                            labelText: 'Address',
                            border: OutlineInputBorder(),
                            prefixIcon: Icon(Icons.home),
                          ),
                          enabled: false,
                          maxLines: 2,
                        ),
                        const SizedBox(height: 24),

                        // Update button (only shown when editing)
                        if (_isEditing) ...[
                          ElevatedButton(
                            onPressed: profileState.isLoading
                                ? null
                                : _handleUpdate,
                            child: profileState.isLoading
                                ? const CircularProgressIndicator()
                                : const Text('Update Profile'),
                          ),
                          const SizedBox(height: 8),
                          OutlinedButton(
                            onPressed: _toggleEdit,
                            child: const Text('Cancel'),
                          ),
                        ],
                      ],
                    ),
                  ),
                ),
    );
  }
}
