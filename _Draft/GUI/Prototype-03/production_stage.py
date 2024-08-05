import pickle
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QFormLayout, QLineEdit, QComboBox, QPushButton, QMessageBox
import pandas as pd

class ProductionStageWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Production Stage")
        self.setGeometry(200, 200, 400, 300)
        layout = QVBoxLayout(self)

        # Load the pickled model
        self.model = self.load_model()

        # Text for Production Stage page
        production_stage_text = QLabel(
            """Provide the following information to estimate emissions for the production stage:
            
1. Select material type.
2. Enter mass used.
3. Enter carbon emission factor.
            """, self)
        layout.addWidget(production_stage_text)

        # Create the form layout
        form_layout = QFormLayout()

        # Create widgets for the form
        self.material_combo = QComboBox()
        self.material_combo.addItems(['Wood', 'Steel', 'Concrete'])  # Example items

        self.mass_input = QLineEdit()
        self.mass_input.setPlaceholderText('Enter mass used')

        self.carbon_factor_input = QLineEdit()
        self.carbon_factor_input.setPlaceholderText('Enter carbon emission factor')

        # Add form widgets to the form layout
        form_layout.addRow('Material Type:', self.material_combo)
        form_layout.addRow('Mass Used:', self.mass_input)
        form_layout.addRow('Carbon Emission Factor:', self.carbon_factor_input)

        # Create a button
        predict_button = QPushButton('Predict')
        predict_button.clicked.connect(self.predict)
        form_layout.addRow(predict_button)

        # Add the form layout to the main layout
        layout.addLayout(form_layout)

        # Label for displaying results
        self.result_label = QLabel("", self)
        layout.addWidget(self.result_label)

