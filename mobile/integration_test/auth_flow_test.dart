import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:move_acces/main.dart' as app;

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  group('Authentication Flow', () {
    testWidgets('Complete login flow', (WidgetTester tester) async {
      // Start app
      app.main();
      await tester.pumpAndSettle();

      // Should be on login screen
      expect(find.text('Move Acces'), findsOneWidget);
      expect(find.text('Login'), findsOneWidget);

      // Enter credentials (using test credentials)
      await tester.enterText(
        find.widgetWithText(TextFormField, 'Email'),
        'diogofebre@gmail.com',
      );
      await tester.enterText(
        find.widgetWithText(TextFormField, 'Password'),
        'TestPassword123!',
      );

      // Tap login
      await tester.tap(find.text('Login'));
      await tester.pumpAndSettle(const Duration(seconds: 3));

      // Should navigate to dashboard (if backend is running and credentials are valid)
      // Note: This test requires a running backend with seeded data
      // In a real scenario, you might want to mock the API calls
      expect(find.text('Dashboard'), findsOneWidget);
    });
  });
}
