from PySide6.QtWidgets import (
    QTextEdit, QTabWidget,
    QApplication, QLabel,
    QHBoxLayout, QVBoxLayout, QWidget, QLabel,
    QTextEdit, QTabWidget, QTableWidget,
    QTableWidgetItem, QHeaderView, QPushButton
)
from coreDesign.default_window import DefaultWindow
import sys

class ModernExample1(DefaultWindow):

    def __init__(self):
        DefaultWindow.__init__(self)

        self.update_title("Modern Example1")
        self.set_content_layout(QHBoxLayout())

        vertical_dock = QWidget()
        vertical_dock.setMaximumWidth(45)
        vertical_dock_right = QWidget()
        vertical_dock_right.setMaximumWidth(45)
        vertical_left_layout = QVBoxLayout(vertical_dock)
        vertical_dock.setStyleSheet("background-color: blue;")
        vertical_dock_right.setStyleSheet("background-color: blue;")
        vertical_left_layout.addWidget(QPushButton("button 1"))
        vertical_left_layout.addWidget(QPushButton("button 2"))
        vertical_left_layout.addWidget(QPushButton("button 3"))

        content_widget = QWidget()
        content_widget.setObjectName("AreaDeConteudo")
        content_widget.setStyleSheet("background-color: red;")
        content_widget.setMouseTracking(True)

        status_bar = QWidget()
        status_bar.setStyleSheet("background-color: rgb(150, 150, 150);")
        status_bar.setMaximumHeight(25)
        self.content_layout.addWidget(vertical_dock)
        self.content_layout.addWidget(content_widget)
        self.content_layout.addWidget(vertical_dock_right)
        self.main_layout.addWidget(status_bar)
        vertical_dock_right.installEventFilter(self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    modern_window = ModernExample1()
    modern_window.show()
    sys.exit(app.exec())