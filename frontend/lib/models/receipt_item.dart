class ReceiptItem {
  final String name;
  final double price;
  final DateTime timestamp;

  ReceiptItem({
    required this.name,
    required this.price,
    required this.timestamp,
  });

  Map<String, dynamic> toMap() {
    return {
      'name': name,
      'price': price,
      'timestamp': timestamp.toIso8601String(),
    };
  }

  static ReceiptItem fromMap(Map<String, dynamic> map) {
    return ReceiptItem(
      name: map['name'],
      price: map['price'],
      timestamp: DateTime.parse(map['timestamp']),
    );
  }
}
