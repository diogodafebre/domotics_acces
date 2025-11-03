import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:dio/dio.dart';
import '../../../core/config/app_config.dart';
import '../../../core/network/dio_client.dart';

/// Auth state
class AuthState {
  final bool isAuthenticated;
  final String? userId;
  final String? email;
  final bool isLoading;
  final String? error;

  const AuthState({
    this.isAuthenticated = false,
    this.userId,
    this.email,
    this.isLoading = false,
    this.error,
  });

  AuthState copyWith({
    bool? isAuthenticated,
    String? userId,
    String? email,
    bool? isLoading,
    String? error,
  }) {
    return AuthState(
      isAuthenticated: isAuthenticated ?? this.isAuthenticated,
      userId: userId ?? this.userId,
      email: email ?? this.email,
      isLoading: isLoading ?? this.isLoading,
      error: error,
    );
  }
}

/// Secure storage provider
final secureStorageProvider = Provider<FlutterSecureStorage>((ref) {
  return const FlutterSecureStorage();
});

/// Dio client provider
final dioClientProvider = Provider<DioClient>((ref) {
  final storage = ref.watch(secureStorageProvider);
  return DioClient(storage);
});

/// Auth provider
class AuthNotifier extends StateNotifier<AuthState> {
  final DioClient _dioClient;
  final FlutterSecureStorage _storage;

  AuthNotifier(this._dioClient, this._storage) : super(const AuthState()) {
    _checkAuthStatus();
  }

  /// Check if user is authenticated
  Future<void> _checkAuthStatus() async {
    final accessToken = await _storage.read(key: AppConfig.accessTokenKey);
    final userId = await _storage.read(key: AppConfig.userIdKey);
    final email = await _storage.read(key: AppConfig.userEmailKey);

    if (accessToken != null && userId != null) {
      state = state.copyWith(
        isAuthenticated: true,
        userId: userId,
        email: email,
      );
    }
  }

  /// Login
  Future<void> login(String email, String password) async {
    state = state.copyWith(isLoading: true, error: null);

    try {
      final response = await _dioClient.dio.post(
        '/auth/login',
        data: {
          'email': email,
          'password': password,
        },
      );

      if (response.statusCode == 200) {
        final data = response.data as Map<String, dynamic>;
        final accessToken = data['access_token'] as String;
        final refreshToken = data['refresh_token'] as String;
        final user = data['user'] as Map<String, dynamic>;

        // Store tokens
        await _storage.write(key: AppConfig.accessTokenKey, value: accessToken);
        await _storage.write(key: AppConfig.refreshTokenKey, value: refreshToken);
        await _storage.write(key: AppConfig.userIdKey, value: user['user_id'].toString());
        await _storage.write(key: AppConfig.userEmailKey, value: user['email'] as String);

        state = state.copyWith(
          isAuthenticated: true,
          userId: user['user_id'].toString(),
          email: user['email'] as String,
          isLoading: false,
        );
      }
    } on DioException catch (e) {
      state = state.copyWith(
        isLoading: false,
        error: e.response?.data?['detail'] ?? 'Login failed',
      );
    } catch (e) {
      state = state.copyWith(
        isLoading: false,
        error: 'An error occurred',
      );
    }
  }

  /// Register
  Future<void> register(Map<String, dynamic> userData) async {
    state = state.copyWith(isLoading: true, error: null);

    try {
      final response = await _dioClient.dio.post(
        '/auth/register',
        data: userData,
      );

      if (response.statusCode == 201) {
        // Auto-login after registration
        await login(userData['email'], userData['password']);
      }
    } on DioException catch (e) {
      state = state.copyWith(
        isLoading: false,
        error: e.response?.data?['detail'] ?? 'Registration failed',
      );
    } catch (e) {
      state = state.copyWith(
        isLoading: false,
        error: 'An error occurred',
      );
    }
  }

  /// Logout
  Future<void> logout() async {
    try {
      final refreshToken = await _storage.read(key: AppConfig.refreshTokenKey);
      if (refreshToken != null) {
        await _dioClient.dio.post(
          '/auth/logout',
          data: {'refresh_token': refreshToken},
        );
      }
    } catch (e) {
      // Ignore logout errors
    }

    // Clear all stored data
    await _storage.deleteAll();

    state = const AuthState();
  }
}

final authProvider = StateNotifierProvider<AuthNotifier, AuthState>((ref) {
  final dioClient = ref.watch(dioClientProvider);
  final storage = ref.watch(secureStorageProvider);
  return AuthNotifier(dioClient, storage);
});
