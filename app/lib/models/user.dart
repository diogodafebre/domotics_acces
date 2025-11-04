/// User model matching backend UserInfo schema
class User {
  final int id;
  final String email;
  final String? prenom;
  final String? nom;

  User({
    required this.id,
    required this.email,
    this.prenom,
    this.nom,
  });

  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      id: json['id'] as int,
      email: json['email'] as String,
      prenom: json['prenom'] as String?,
      nom: json['nom'] as String?,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'email': email,
      'prenom': prenom,
      'nom': nom,
    };
  }

  String get fullName {
    final parts = [prenom, nom].where((p) => p != null && p.isNotEmpty);
    return parts.isEmpty ? email : parts.join(' ');
  }
}
