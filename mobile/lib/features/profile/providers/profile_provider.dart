import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:dio/dio.dart';
import '../../auth/providers/auth_provider.dart';

/// User profile model
class UserProfile {
  final int userId;
  final String email;
  final String prenom;
  final String nom;
  final String dateNaissance;
  final String rue;
  final String npa;
  final String localite;
  final String? tel;

  UserProfile({
    required this.userId,
    required this.email,
    required this.prenom,
    required this.nom,
    required this.dateNaissance,
    required this.rue,
    required this.npa,
    required this.localite,
    this.tel,
  });

  factory UserProfile.fromJson(Map<String, dynamic> json) {
    return UserProfile(
      userId: json['user_id'] as int,
      email: json['email'] as String,
      prenom: json['prenom'] as String,
      nom: json['nom'] as String,
      dateNaissance: json['date_naissance'] as String,
      rue: json['rue'] as String,
      npa: json['npa'] as String,
      localite: json['localite'] as String,
      tel: json['tel'] as String?,
    );
  }
}

/// Profile state
class ProfileState {
  final UserProfile? profile;
  final bool isLoading;
  final String? error;

  const ProfileState({
    this.profile,
    this.isLoading = false,
    this.error,
  });

  ProfileState copyWith({
    UserProfile? profile,
    bool? isLoading,
    String? error,
  }) {
    return ProfileState(
      profile: profile ?? this.profile,
      isLoading: isLoading ?? this.isLoading,
      error: error,
    );
  }
}

/// Profile provider
class ProfileNotifier extends StateNotifier<ProfileState> {
  final Ref _ref;

  ProfileNotifier(this._ref) : super(const ProfileState());

  /// Fetch profile
  Future<void> fetchProfile() async {
    state = state.copyWith(isLoading: true, error: null);

    try {
      final dioClient = _ref.read(dioClientProvider);
      final response = await dioClient.dio.get('/users/me');

      if (response.statusCode == 200) {
        final profile = UserProfile.fromJson(response.data);
        state = state.copyWith(profile: profile, isLoading: false);
      }
    } on DioException catch (e) {
      state = state.copyWith(
        isLoading: false,
        error: e.response?.data?['detail'] ?? 'Failed to load profile',
      );
    } catch (e) {
      state = state.copyWith(
        isLoading: false,
        error: 'An error occurred',
      );
    }
  }

  /// Update profile
  Future<void> updateProfile(Map<String, dynamic> data) async {
    state = state.copyWith(isLoading: true, error: null);

    try {
      final dioClient = _ref.read(dioClientProvider);
      final response = await dioClient.dio.patch('/users/me', data: data);

      if (response.statusCode == 200) {
        final profile = UserProfile.fromJson(response.data);
        state = state.copyWith(profile: profile, isLoading: false);
      }
    } on DioException catch (e) {
      state = state.copyWith(
        isLoading: false,
        error: e.response?.data?['detail'] ?? 'Failed to update profile',
      );
    } catch (e) {
      state = state.copyWith(
        isLoading: false,
        error: 'An error occurred',
      );
    }
  }
}

final profileProvider = StateNotifierProvider<ProfileNotifier, ProfileState>(
  (ref) => ProfileNotifier(ref),
);
