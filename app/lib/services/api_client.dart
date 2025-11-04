import 'package:dio/dio.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import '../models/user.dart';

/// API client for Domotics backend with JWT authentication
class ApiClient {
  static const String _accessTokenKey = 'access_token';
  static const String _refreshTokenKey = 'refresh_token';

  late final Dio _dio;
  final FlutterSecureStorage _storage = const FlutterSecureStorage();
  final String baseUrl;

  // Callback when user needs to re-authenticate
  Function()? onUnauthorized;

  ApiClient({required this.baseUrl}) {
    _dio = Dio(BaseOptions(
      baseUrl: baseUrl,
      connectTimeout: const Duration(seconds: 10),
      receiveTimeout: const Duration(seconds: 10),
      headers: {
        'Content-Type': 'application/json',
      },
    ));

    // Add interceptor to automatically add Authorization header
    _dio.interceptors.add(
      InterceptorsWrapper(
        onRequest: (options, handler) async {
          // Add access token to all requests
          final token = await getAccessToken();
          if (token != null) {
            options.headers['Authorization'] = 'Bearer $token';
          }
          handler.next(options);
        },
        onError: (error, handler) async {
          // Handle 401 errors with token refresh
          if (error.response?.statusCode == 401) {
            // Try to refresh the token
            final refreshed = await _refreshToken();
            if (refreshed) {
              // Retry the original request with new token
              final token = await getAccessToken();
              error.requestOptions.headers['Authorization'] = 'Bearer $token';
              final response = await _dio.fetch(error.requestOptions);
              return handler.resolve(response);
            } else {
              // Refresh failed, logout user
              await logout();
              onUnauthorized?.call();
            }
          }
          handler.next(error);
        },
      ),
    );
  }

  /// Login with email and password
  Future<User> login(String email, String password) async {
    try {
      final response = await _dio.post(
        '/auth/login',
        data: {
          'email': email,
          'password': password,
        },
      );

      // Save tokens
      await _storage.write(key: _accessTokenKey, value: response.data['access']);
      await _storage.write(key: _refreshTokenKey, value: response.data['refresh']);

      // Return user info
      return User.fromJson(response.data['user']);
    } on DioException catch (e) {
      if (e.response?.statusCode == 401) {
        throw Exception('Identifiants invalides');
      }
      throw Exception('Erreur de connexion: ${e.message}');
    }
  }

  /// Refresh access token using refresh token
  Future<bool> _refreshToken() async {
    try {
      final refreshToken = await getRefreshToken();
      if (refreshToken == null) return false;

      final response = await _dio.post(
        '/auth/refresh',
        data: {'refresh': refreshToken},
      );

      // Save new access token
      await _storage.write(key: _accessTokenKey, value: response.data['access']);
      return true;
    } catch (e) {
      return false;
    }
  }

  /// Get current user information
  Future<User> getCurrentUser() async {
    try {
      final response = await _dio.get('/auth/me');
      return User.fromJson(response.data);
    } on DioException catch (e) {
      if (e.response?.statusCode == 401) {
        throw Exception('Non authentifié');
      }
      throw Exception('Erreur lors de la récupération du profil');
    }
  }

  /// Logout - clear all stored tokens
  Future<void> logout() async {
    await _storage.delete(key: _accessTokenKey);
    await _storage.delete(key: _refreshTokenKey);
  }

  /// Get stored access token
  Future<String?> getAccessToken() async {
    return await _storage.read(key: _accessTokenKey);
  }

  /// Get stored refresh token
  Future<String?> getRefreshToken() async {
    return await _storage.read(key: _refreshTokenKey);
  }

  /// Check if user has valid tokens
  Future<bool> hasTokens() async {
    final accessToken = await getAccessToken();
    return accessToken != null;
  }
}
