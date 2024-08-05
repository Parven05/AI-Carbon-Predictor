from PySide6.QtWidgets import QApplication, QMainWindow, QMenuBar
from PySide6.QtGui import QAction
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Carbon Predictor")
        self.setGeometry(100, 100, 910, 600)

        # Create the menu bar
        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)

        # Creating menu actions
        buttons = [
            "Get Started",
            "Production Stage",
            "Transportation to Factory Stage",
            "Manufacturing Stage",
            "Transportation to Site Stage",
            "Construction Stage",
            "Total Carbon Emission"
        ]

        for btn_text in buttons:
            action = QAction(btn_text, self)
            action.triggered.connect(lambda _, text=btn_text: self.on_button_clicked(text))
            menu_bar.addAction(action)

    def on_button_clicked(self, button_name):
        print(f"{button_name} menu item clicked")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
