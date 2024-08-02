from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QStackedWidget, QListWidget, QListWidgetItem
from PySide6.QtCore import Qt
from GUI.widgets import HomeWidget, PredictWidget
from Utils.constants import ENCODING_MAP, TOTAL_FEATURES
from GUI.styles import MAIN_WINDOW_STYLE  # Correct import

class MainWindow(QMainWindow):
    def __init__(self, model_handler):
        super().__init__()
        self.model_handler = model_handler

        # Set up the GUI
        self.setWindowTitle('Prediction App')
        self.setGeometry(100, 100, 400, 400)

        # Create main widget and layout
        main_widget = QWidget()
        main_layout = QHBoxLayout()

        # Sidebar menu
        self.sidebar = QListWidget()
        self.sidebar.setFixedWidth(60)
        self.sidebar.setStyleSheet(MAIN_WINDOW_STYLE)  # Apply style
        sidebar_items = ['Home', 'A1', 'A2', 'A3', 'A4']
        for item in sidebar_items:
            list_item = QListWidgetItem(item[:2].upper())  # Show only the first two letters in uppercase
            list_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.sidebar.addItem(list_item)
        self.sidebar.currentItemChanged.connect(self.on_sidebar_item_changed)
        main_layout.addWidget(self.sidebar)

        # Central widget and layout
        self.stacked_widget = QStackedWidget()
        self.home_widget = HomeWidget()
        self.predict_widget = PredictWidget(self.model_handler, ENCODING_MAP)
        self.settings_widget = QWidget()  # Implement settings widget
        self.help_widget = QWidget()      # Implement help widget
        self.about_widget = QWidget()     # Implement about widget

        self.stacked_widget.addWidget(self.home_widget)
        self.stacked_widget.addWidget(self.predict_widget)
        self.stacked_widget.addWidget(self.settings_widget)
        self.stacked_widget.addWidget(self.help_widget)
        self.stacked_widget.addWidget(self.about_widget)

        main_layout.addWidget(self.stacked_widget)

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def on_sidebar_item_changed(self, current, previous):
        if current is not None:
            if current.text() == 'HO':
                self.stacked_widget.setCurrentWidget(self.home_widget)
            elif current.text() == 'A1':
                self.reset_predict_page()
                self.stacked_widget.setCurrentWidget(self.predict_widget)
            elif current.text() == 'A2':
                self.stacked_widget.setCurrentWidget(self.settings_widget)
            elif current.text() == 'A3':
                self.stacked_widget.setCurrentWidget(self.help_widget)
            elif current.text() == 'A4':
                self.stacked_widget.setCurrentWidget(self.about_widget)

    def reset_predict_page(self):
        self.predict_widget.categorical_dropdown.setCurrentIndex(0)
        self.predict_widget.mass_input.clear()
        self.predict_widget.emission_input.clear()
        self.predict_widget.result_label.setText('')