import 'dart:async';
import 'package:dio/dio.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import '../config/app_config.dart';

/// Dio HTTP client with auth interceptor
class DioClient {
  late final Dio _dio;
  final FlutterSecureStorage _storage;
  final _requestQueue = <RequestOptions>[];
  bool _isRefreshing = false;

  DioClient(this._storage) {
    _dio = Dio(
      BaseOptions(
        baseUrl: AppConfig.apiBaseUrl,
        connectTimeout: AppConfig.connectTimeout,
        receiveTimeout: AppConfig.receiveTimeout,
        sendTimeout: AppConfig.sendTimeout,
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
      ),
    );

    _dio.interceptors.add(
      InterceptorsWrapper(
        onRequest: _onRequest,
        onError: _onError,
      ),
    );
  }

  Dio get dio => _dio;

  /// Add auth token to requests
  Future<void> _onRequest(
    RequestOptions options,
    RequestInterceptorHandler handler,
  ) async {
    // Skip auth for login/register endpoints
    if (options.path.contains('/auth/login') ||
        options.path.contains('/auth/register') ||
        options.path.contains('/auth/refresh')) {
      return handler.next(options);
    }

    // Add access token
    final token = await _storage.read(key: AppConfig.accessTokenKey);
    if (token != null) {
      options.headers['Authorization'] = 'Bearer $token';
    }

    handler.next(options);
  }

  /// Handle 401 errors with token refresh
  Future<void> _onError(
    DioException err,
    ErrorInterceptorHandler handler,
  ) async {
    if (err.response?.statusCode == 401) {
      // Try to refresh token
      final refreshed = await _refreshToken();
      if (refreshed) {
        // Retry original request
        try {
          final response = await _retry(err.requestOptions);
          return handler.resolve(response);
        } catch (e) {
          return handler.reject(err);
        }
      } else {
        // Refresh failed, clear tokens
        await _clearAuth();
        return handler.reject(err);
      }
    }

    handler.next(err);
  }

  /// Refresh access token
  Future<bool> _refreshToken() async {
    if (_isRefreshing) {
      // Wait for current refresh to complete
      await Future.delayed(const Duration(milliseconds: 100));
      return _refreshToken();
    }

    _isRefreshing = true;

    try {
      final refreshToken = await _storage.read(key: AppConfig.refreshTokenKey);
      if (refreshToken == null) {
        return false;
      }

      final response = await _dio.post(
        '/auth/refresh',
        data: {'refresh_token': refreshToken},
      );

      if (response.statusCode == 200) {
        final data = response.data as Map<String, dynamic>;
        final newAccessToken = data['access_token'] as String;

        await _storage.write(
          key: AppConfig.accessTokenKey,
          value: newAccessToken,
        );

        return true;
      }

      return false;
    } catch (e) {
      return false;
    } finally {
      _isRefreshing = false;
    }
  }

  /// Retry failed request with new token
  Future<Response> _retry(RequestOptions requestOptions) async {
    final token = await _storage.read(key: AppConfig.accessTokenKey);
    if (token != null) {
      requestOptions.headers['Authorization'] = 'Bearer $token';
    }

    final options = Options(
      method: requestOptions.method,
      headers: requestOptions.headers,
    );

    return _dio.request(
      requestOptions.path,
      data: requestOptions.data,
      queryParameters: requestOptions.queryParameters,
      options: options,
    );
  }

  /// Clear authentication data
  Future<void> _clearAuth() async {
    await _storage.delete(key: AppConfig.accessTokenKey);
    await _storage.delete(key: AppConfig.refreshTokenKey);
    await _storage.delete(key: AppConfig.userIdKey);
    await _storage.delete(key: AppConfig.userEmailKey);
  }
}
