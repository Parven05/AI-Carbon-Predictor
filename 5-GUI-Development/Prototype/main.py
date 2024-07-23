import sys
from PySide6.QtWidgets import QApplication
from model_handler import ModelHandler
from gui.main_window import MainWindow
from utils.constants import TOTAL_FEATURES

if __name__ == '__main__':
    model_path = 'Gradient-Boosting-A1.pkcls'

    model_handler = ModelHandler(model_path, TOTAL_FEATURES)

    app = QApplication(sys.argv)
    window = MainWindow(model_handler)
    window.show()
    sys.exit(app.exec())
