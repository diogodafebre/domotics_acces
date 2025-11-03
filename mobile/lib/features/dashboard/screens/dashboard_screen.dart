import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../auth/providers/auth_provider.dart';
import '../../../services/websocket_service.dart';

class DashboardScreen extends ConsumerStatefulWidget {
  const DashboardScreen({super.key});

  @override
  ConsumerState<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends ConsumerState<DashboardScreen> {
  WebSocketService? _wsService;
  String? _lastMessage;

  @override
  void initState() {
    super.initState();
    _initWebSocket();
  }

  Future<void> _initWebSocket() async {
    final storage = ref.read(secureStorageProvider);
    _wsService = WebSocketService(storage);
  }

  Future<void> _connectWebSocket() async {
    if (_wsService == null) return;

    await _wsService!.connect();
    _wsService!.messages.listen((message) {
      if (mounted) {
        setState(() {
          _lastMessage = message.toString();
        });
      }
    });
  }

  void _sendEcho() {
    _wsService?.sendEcho('Hello from Flutter!');
  }

  @override
  void dispose() {
    _wsService?.disconnect();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final authState = ref.watch(authProvider);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Dashboard'),
        actions: [
          IconButton(
            icon: const Icon(Icons.settings),
            onPressed: () => context.push('/settings'),
          ),
        ],
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // Welcome card
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Bonjour ${authState.email ?? "User"}!',
                      style: Theme.of(context).textTheme.headlineSmall,
                    ),
                    const SizedBox(height: 8),
                    Text(
                      'Welcome to Move Acces',
                      style: Theme.of(context).textTheme.bodyLarge,
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 16),

            // Quick actions
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Quick Actions',
                      style: Theme.of(context).textTheme.titleMedium,
                    ),
                    const SizedBox(height: 16),
                    ListTile(
                      leading: const Icon(Icons.person),
                      title: const Text('View Profile'),
                      trailing: const Icon(Icons.chevron_right),
                      onTap: () => context.push('/profile'),
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 16),

            // WebSocket test
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'WebSocket Test',
                      style: Theme.of(context).textTheme.titleMedium,
                    ),
                    const SizedBox(height: 16),
                    ElevatedButton(
                      onPressed: _connectWebSocket,
                      child: const Text('Connect WebSocket'),
                    ),
                    const SizedBox(height: 8),
                    ElevatedButton(
                      onPressed: _sendEcho,
                      child: const Text('Send Echo'),
                    ),
                    const SizedBox(height: 8),
                    if (_lastMessage != null)
                      Text(
                        'Last message: $_lastMessage',
                        style: Theme.of(context).textTheme.bodySmall,
                      ),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
