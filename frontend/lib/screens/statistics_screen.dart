import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';
import '../services/database_service.dart';

class StatisticsScreen extends StatelessWidget {
  final DatabaseService _databaseService = DatabaseService();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Statistics'),
      ),
      body: FutureBuilder<List<Map<String, dynamic>>>(
        future: _databaseService.getExpenses(),
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return Center(child: CircularProgressIndicator());
          } else if (snapshot.hasError) {
            return Center(child: Text('Error: ${snapshot.error}'));
          } else if (!snapshot.hasData || snapshot.data!.isEmpty) {
            return Center(child: Text('No data available'));
          }

          final data = snapshot.data!;
          final barGroups = data.map((expense) {
            return BarChartGroupData(
              x: expense['name'].hashCode,
              barRods: [
                BarChartRodData(
                  toY: expense['price'].toDouble(),
                  color: Colors.blue,
                ),
              ],
            );
          }).toList();

          return Padding(
            padding: const EdgeInsets.all(8.0),
            child: BarChart(
              BarChartData(
                barGroups: barGroups,
                titlesData: FlTitlesData(
                  bottomTitles: AxisTitles(
                    sideTitles: SideTitles(
                      showTitles: true,
                      getTitlesWidget: (value, meta) {
                        final expense = data.firstWhere(
                          (expense) => expense['name'].hashCode == value.toInt(),
                          orElse: () => {'name': ''},
                        );
                        return Padding(
                          padding: const EdgeInsets.only(top: 8.0),
                          child: Text(expense['name']),
                        );
                      },
                    ),
                  ),
                  leftTitles: AxisTitles(
                    sideTitles: SideTitles(
                      showTitles: true,
                      getTitlesWidget: (value, meta) {
                        return Text(value.toString());
                      },
                    ),
                  ),
                ),
                borderData: FlBorderData(
                  show: true,
                  border: Border.all(color: Colors.black, width: 1),
                ),
              ),
            ),
          );
        },
      ),
    );
  }
}
