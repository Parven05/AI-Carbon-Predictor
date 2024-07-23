from PySide6.QtWidgets import QWidget, QVBoxLayout, QComboBox, QLineEdit, QPushButton, QLabel
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
from gui.styles import MAIN_WINDOW_STYLE

class HomeWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        title_label = QLabel('A1 Production Prediction')
        title_label.setFont(QFont('Arial', 16, QFont.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        layout.addStretch()
        self.setLayout(layout)

class PredictWidget(QWidget):
    def __init__(self, model_handler, encoding_map):
        super().__init__()
        self.model_handler = model_handler
        self.encoding_map = encoding_map
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        title_label = QLabel('Prediction Page')
        title_label.setFont(QFont('Arial', 16, QFont.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        self.categorical_dropdown = QComboBox()
        self.categorical_dropdown.addItems(['cement', 'wood', 'steel'])
        self.categorical_dropdown.setStyleSheet(MAIN_WINDOW_STYLE)
        layout.addWidget(self.categorical_dropdown)

        self.mass_input = QLineEdit()
        self.mass_input.setPlaceholderText('Enter mass used')
        self.mass_input.setStyleSheet(MAIN_WINDOW_STYLE)
        layout.addWidget(self.mass_input)

        self.emission_input = QLineEdit()
        self.emission_input.setPlaceholderText('Enter carbon emission factor')
        self.emission_input.setStyleSheet(MAIN_WINDOW_STYLE)
        layout.addWidget(self.emission_input)

        self.predict_button = QPushButton('Predict')
        self.predict_button.setStyleSheet(MAIN_WINDOW_STYLE)
        self.predict_button.clicked.connect(self.predict)
        layout.addWidget(self.predict_button)

        self.result_label = QLabel('')
        self.result_label.setStyleSheet(MAIN_WINDOW_STYLE)
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.result_label)

        layout.addStretch()
        self.setLayout(layout)

    def predict(self):
        try:
            categorical_value = self.categorical_dropdown.currentText()
            numeric_feature1 = float(self.mass_input.text())
            numeric_feature2 = float(self.emission_input.text())

            prediction = self.model_handler.predict(categorical_value, [numeric_feature1, numeric_feature2], self.encoding_map)
            self.result_label.setText(f"Prediction: {prediction[0]}")
        except ValueError as e:
            self.result_label.setText(f"Invalid input: {e}")
