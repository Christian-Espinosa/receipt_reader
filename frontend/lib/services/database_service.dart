import 'package:sqflite/sqflite.dart';
import 'package:path/path.dart';
import '../models/receipt_item.dart'; 

class DatabaseService {
  static final DatabaseService _instance = DatabaseService._internal();
  factory DatabaseService() => _instance;
  DatabaseService._internal();

  Database? _database;

  Future<Database> get database async {
    if (_database != null) return _database!;
    _database = await _initDatabase();
    return _database!;
  }

  Future<Database> _initDatabase() async {
    String path = join(await getDatabasesPath(), 'receipts.db');
    return await openDatabase(
      path,
      version: 1,
      onCreate: (db, version) async {
        await db.execute(
          'CREATE TABLE receipts(id INTEGER PRIMARY KEY, name TEXT, price REAL, timestamp TEXT)',
        );
      },
    );
  }

  Future<void> insertReceiptItem(ReceiptItem item) async {
    final db = await database;
    await db.insert(
      'receipts',
      item.toMap(),
      conflictAlgorithm: ConflictAlgorithm.replace,
    );
  }

  Future<List<ReceiptItem>> getReceiptItems() async {
    final db = await database;
    final List<Map<String, dynamic>> maps = await db.query('receipts');

    return List.generate(maps.length, (i) {
      return ReceiptItem.fromMap(maps[i]);
    });
  }

  Future<void> insertExpense(String name, double price) async {
    final timestamp = DateTime.now();
    final item = ReceiptItem(name: name, price: price, timestamp: timestamp);
    await insertReceiptItem(item);
  }

  Future<List<Map<String, dynamic>>> getExpenses() async {
    final db = await database;
    return await db.query('receipts');
  }
}
