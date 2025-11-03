# Move Acces Mobile

Flutter mobile application for Move Acces.

## Features

- **Authentication**: JWT-based login with token refresh
- **Profile Management**: View and edit user profile
- **WebSocket**: Real-time communication
- **Secure Storage**: Encrypted token storage
- **Offline Support**: Basic offline caching with Drift/SQLite
- **State Management**: Riverpod
- **Routing**: go_router with auth guards

## Requirements

- Flutter SDK 3.2.0+
- Dart 3.2.0+
- Android Studio / Xcode (for mobile builds)

## Installation

```bash
# Install dependencies
flutter pub get

# Run code generation (if needed)
flutter pub run build_runner build --delete-conflicting-outputs
```

## Configuration

The app reads the API base URL from build arguments:

```bash
flutter run --dart-define=API_BASE_URL=https://api.yourdomain.com
```

For development with local backend:

```bash
flutter run --dart-define=API_BASE_URL=http://10.0.2.2:8080  # Android emulator
flutter run --dart-define=API_BASE_URL=http://localhost:8080  # iOS simulator
```

## Running

```bash
# Run on connected device/emulator
flutter run

# Run with API configuration
flutter run --dart-define=API_BASE_URL=http://localhost:8080

# Run on specific device
flutter devices
flutter run -d <device-id>
```

## Testing

```bash
# Run unit and widget tests
flutter test

# Run integration tests (requires running backend)
flutter test integration_test/auth_flow_test.dart
```

## Building

### Android

```bash
# Debug APK
flutter build apk --debug

# Release APK
flutter build apk --release --dart-define=API_BASE_URL=https://api.yourdomain.com

# App Bundle (for Play Store)
flutter build appbundle --release --dart-define=API_BASE_URL=https://api.yourdomain.com
```

### iOS

```bash
# Debug build
flutter build ios --debug

# Release build
flutter build ios --release --dart-define=API_BASE_URL=https://api.yourdomain.com
```

## Project Structure

```
lib/
├── core/
│   ├── config/          # App configuration
│   └── network/         # HTTP client (Dio)
├── features/
│   ├── auth/           # Authentication
│   ├── dashboard/      # Dashboard
│   ├── profile/        # User profile
│   └── settings/       # Settings
├── services/           # Services (WebSocket, etc.)
├── common/             # Common widgets
└── db/                 # Local database (Drift)
```

## Key Dependencies

- **flutter_riverpod**: State management
- **go_router**: Routing and navigation
- **dio**: HTTP client
- **flutter_secure_storage**: Secure token storage
- **web_socket_channel**: WebSocket communication
- **drift**: Local SQLite database

## Linting & Formatting

```bash
# Analyze code
flutter analyze

# Format code
dart format .
```

## Troubleshooting

### Android Network Issues

If you can't connect to localhost backend from Android emulator:
- Use `10.0.2.2` instead of `localhost`
- Ensure backend allows connections from emulator

### iOS Network Issues

iOS requires HTTPS or explicit HTTP exceptions in Info.plist for development.

### Token Refresh Issues

If experiencing auth issues:
1. Clear app data
2. Logout and login again
3. Check backend logs for token validation errors
