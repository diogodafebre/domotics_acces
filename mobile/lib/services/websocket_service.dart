import 'dart:async';
import 'dart:convert';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:web_socket_channel/web_socket_channel.dart';
import '../core/config/app_config.dart';

/// WebSocket service for real-time communication
class WebSocketService {
  final FlutterSecureStorage _storage;
  WebSocketChannel? _channel;
  final _messageController = StreamController<Map<String, dynamic>>.broadcast();

  WebSocketService(this._storage);

  /// Stream of messages from server
  Stream<Map<String, dynamic>> get messages => _messageController.stream;

  /// Connect to WebSocket server
  Future<void> connect() async {
    final token = await _storage.read(key: AppConfig.accessTokenKey);
    if (token == null) {
      throw Exception('No access token available');
    }

    final wsUrl = '${AppConfig.wsUrl}?token=$token';
    _channel = WebSocketChannel.connect(Uri.parse(wsUrl));

    _channel!.stream.listen(
      (data) {
        try {
          final message = json.decode(data as String) as Map<String, dynamic>;
          _messageController.add(message);
        } catch (e) {
          // Ignore invalid messages
        }
      },
      onError: (error) {
        _messageController.addError(error);
      },
      onDone: () {
        // Connection closed
      },
    );
  }

  /// Send echo message
  void sendEcho(String payload) {
    if (_channel != null) {
      final message = json.encode({
        'type': 'echo',
        'payload': payload,
      });
      _channel!.sink.add(message);
    }
  }

  /// Send ping
  void sendPing() {
    if (_channel != null) {
      final message = json.encode({'type': 'ping'});
      _channel!.sink.add(message);
    }
  }

  /// Disconnect from WebSocket
  void disconnect() {
    _channel?.sink.close();
    _messageController.close();
  }
}
