import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';
import 'package:intl/intl.dart';

class HomeScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Home Screen'),
      ),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: LineChartWidget(),
        ),
      ),
    );
  }
}

class LineChartWidget extends StatelessWidget {
  final List<DateTime> dates = [
    DateTime(2024, 6, 19),
    DateTime(2024, 6, 5),
    DateTime(2023, 11, 10),
    DateTime(2023, 11, 15),
    DateTime(2023, 9, 20),
    DateTime(2023, 11, 7),
  ];

  final List<double> values = [
    21.55,
    8.72,
    33.35,
    22.01,
    15.80,
    19.60,
  ];

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      height: 300,
      child: LineChart(
        LineChartData(
          borderData: FlBorderData(
            show: true,
            border: Border.all(color: Colors.black, width: 1),
          ),
          titlesData: FlTitlesData(
            bottomTitles: AxisTitles(
              sideTitles: SideTitles(
                showTitles: true,
                interval: 1,
                getTitlesWidget: (value, meta) {
                  final index = value.toInt();
                  if (index < 0 || index >= dates.length) {
                    return const SizedBox.shrink();
                  }
                  final date = dates[index];
                  return SideTitleWidget(
                    axisSide: meta.axisSide,
                    space: 4.0,
                    child: Text(
                      DateFormat('dd/MM/yyyy').format(date),
                      style: TextStyle(fontSize: 10),
                    ),
                  );
                },
                reservedSize: 40,
              ),
            ),
            leftTitles: AxisTitles(
              sideTitles: SideTitles(
                showTitles: true,
                interval: 10,
                getTitlesWidget: (value, meta) {
                  return Text(
                    value.toString(),
                    style: const TextStyle(
                      color: Colors.black,
                      fontWeight: FontWeight.bold,
                      fontSize: 12,
                    ),
                  );
                },
                reservedSize: 40,
              ),
            ),
          ),
          lineBarsData: [
            LineChartBarData(
              spots: List.generate(dates.length, (index) {
                return FlSpot(index.toDouble(), values[index]);
              }),
              isCurved: true,
              color: Colors.blue,
              barWidth: 4,
              belowBarData: BarAreaData(show: false),
              dotData: FlDotData(show: true),
            ),
          ],
          gridData: FlGridData(show: true),
        ),
      ),
    );
  }
}
