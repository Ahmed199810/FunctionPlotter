from PySide2.QtWidgets import *
from PySide2.QtCore import Slot, Qt
import re
import numpy as np
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
matplotlib.use('Qt5Agg')

# app variables
eqn = ""


replacements = {
    '^': '**',
}
allowed_words = [
    'x',
]

def show_message(msg):
    dialog = QMessageBox()
    dialog.setText(msg)
    dialog.setWindowTitle("Alert !")
    dialog.exec_()

# a function to convert string input to equation command
def validate_input(eqn):
    for word in re.findall('[a-zA-Z_]+', eqn):
        if word not in allowed_words:
            show_message("Enter a function of x only")
            return False
    return True

def convert_string_to_equation(eqn):
    #check for white spaces
    eqn = eqn.replace(" ", "")
    txt_eqn.setText(eqn)

    # validate the input
    if validate_input(eqn):
        for old, new in replacements.items():
            eqn = eqn.replace(old, new)

        def func(x):
            return eval(eqn)

        return func
    return ""

# function to call the plotter
def updateCanvas(can):
    global canvas
    canvas = can


def plot_equation(eqn, min_v, max_v):
    y = convert_string_to_equation(eqn)
    if y != "":
        x = np.linspace(float(min_v), float(max_v), 250)
        fig = Figure(figsize=(600, 600), dpi=70, facecolor=(1, 1, 1), edgecolor=(0, 0, 0))
        ax = fig.add_subplot(111)
        ax.plot(x, y(x))
        can = FigureCanvas(fig)
        layout.replaceWidget(canvas, can)
        updateCanvas(can)



# plot button event
@Slot()
def btnClickRes():
    eqn = txt_eqn.text()
    min_val = txt_min_val.text()
    max_val = txt_max_val.text()

    if eqn == "":
        show_message("Enter a function f(x)")
    elif min_val == "":
        show_message("Enter the Min Value of x")
    elif max_val == "":
        show_message("Enter the Max Value of x")
    else:
        plot_equation(eqn, min_val, max_val)


# init the Application
app = QApplication([])
window = QWidget()
layout = QVBoxLayout()
control_container = QVBoxLayout()


# the application widgets
btnPlot = QPushButton("Plot")
txt_eqn = QLineEdit()
txt_min_val = QLineEdit()
txt_max_val = QLineEdit()
txt_label = QLabel()
txt_label_graph = QLabel()
line = QWidget()
fig = Figure(figsize=(600, 600), dpi=70, facecolor=(1, 1, 1), edgecolor=(0, 0, 0))
ax = fig.add_subplot(111)
canvas = FigureCanvas(fig)


# widgets properties
btnPlot.clicked.connect(btnClickRes)
txt_eqn.setPlaceholderText("Enter a Function of x, f(x) = ")
txt_min_val.setPlaceholderText("enter the min val of x")
txt_max_val.setPlaceholderText("enter the max val of x")
txt_min_val.setFixedWidth(150)
txt_max_val.setFixedWidth(150)
btnPlot.setFixedWidth(150)
txt_label.setText("Equation Plotter")
txt_label_graph.setText("Graph")
line.setFixedHeight(2)

# widgets styling
btnPlot.setStyleSheet(
    "border-radius: 4px;"
    "background-color: #3a7ae0;"
    "border: none;"
    "color: white;"
    "padding: 15px 32px;"
    "text-align: center;"
    "text-decoration: none;"
    "display: inline-block;"
    "font-size: 16px;"
    "transition-duration: 0.4s;"
    "font-size: 12px;"
)

txt_eqn.setStyleSheet(
    "border: 2px solid gray;"
    "border-radius: 4px;"
    "padding: 8px"
)
txt_min_val.setStyleSheet(
    "border: 2px solid gray;"
    "border-radius: 4px;"
    "padding: 8px"
)
txt_max_val.setStyleSheet(
    "border: 2px solid gray;"
    "border-radius: 4px;"
    "padding: 8px"
)
txt_label.setStyleSheet(
    "color: #000;"
    "font-size: 20px;"
)
txt_label_graph.setStyleSheet(
    "color: #000;"
    "font-size: 13px;"
)
line.setStyleSheet(
    "background-color: #757575"
)


# add widgets
control_container.addWidget(txt_label)
control_container.addWidget(txt_eqn)
control_container.addWidget(txt_min_val)
control_container.addWidget(txt_max_val)
control_container.addWidget(btnPlot)
control_container.addWidget(line)
control_container.addWidget(txt_label_graph)

control_container.setAlignment(Qt.AlignTop)

layout.addLayout(control_container)
layout.addWidget(canvas)
window.setLayout(layout)
window.setWindowTitle("Equation Plotter")
window.resize(700, 500)
window.show()

app.exec_()