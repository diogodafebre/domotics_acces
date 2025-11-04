import 'package:flutter/foundation.dart';
import '../models/user.dart';
import '../services/api_client.dart';

/// Authentication state management using Provider
class AuthState extends ChangeNotifier {
  User? _user;
  ApiClient? _apiClient;
  bool _isLoading = false;
  String? _error;

  User? get user => _user;
  bool get isAuthenticated => _user != null;
  bool get isLoading => _isLoading;
  String? get error => _error;

  /// Initialize API client with base URL
  void initApiClient(String baseUrl) {
    _apiClient = ApiClient(baseUrl: baseUrl);
    _apiClient!.onUnauthorized = logout;
    _checkExistingAuth();
  }

  /// Check if user has existing valid tokens on app start
  Future<void> _checkExistingAuth() async {
    if (_apiClient == null) return;

    final hasTokens = await _apiClient!.hasTokens();
    if (hasTokens) {
      try {
        _user = await _apiClient!.getCurrentUser();
        notifyListeners();
      } catch (e) {
        // Token invalid, ignore and show login
        await logout();
      }
    }
  }

  /// Login with email and password
  Future<bool> login(String email, String password) async {
    if (_apiClient == null) {
      _error = 'API client not initialized';
      notifyListeners();
      return false;
    }

    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      _user = await _apiClient!.login(email, password);
      _isLoading = false;
      notifyListeners();
      return true;
    } catch (e) {
      _error = e.toString().replaceFirst('Exception: ', '');
      _isLoading = false;
      notifyListeners();
      return false;
    }
  }

  /// Logout and clear all data
  Future<void> logout() async {
    await _apiClient?.logout();
    _user = null;
    _error = null;
    notifyListeners();
  }

  /// Fetch current user data (for dashboard refresh)
  Future<void> fetchCurrentUser() async {
    if (_apiClient == null) return;

    try {
      _user = await _apiClient!.getCurrentUser();
      notifyListeners();
    } catch (e) {
      _error = e.toString().replaceFirst('Exception: ', '');
      notifyListeners();
    }
  }

  /// Clear error message
  void clearError() {
    _error = null;
    notifyListeners();
  }
}
