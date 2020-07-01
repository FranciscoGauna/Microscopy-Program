from PyQt5.QtChart import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

a = QApplication([])

set0 = QBarSet("Jane")

categories = []

for i in range(360):
    set0.insert(i, i+2)
    categories.append(str(i))

series = QBarSeries()
series.append(set0)

chart = QChart()
chart.addSeries(series)
chart.setTitle("Simple bar chart example")
chart.setAnimationOptions(QChart.SeriesAnimations)

axis = QBarCategoryAxis()
axis.append(categories)
chart.createDefaultAxes()
chart.setAxisX(axis, series)

chart.legend().setVisible(True)
chart.legend().setAlignment(Qt.AlignBottom)

chartView = QChartView(chart)
chartView.setRenderHint(QPainter.Antialiasing)

window = QMainWindow()
window.setCentralWidget(chartView)
window.resize(420, 300)
window.show()

a.exec_()
