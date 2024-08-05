import pickle
from PySide6.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QFormLayout, QLineEdit, QComboBox, QPushButton, QMessageBox, QLabel
from PySide6.QtGui import QIcon
import pandas as pd

class ConstructionStageWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Construction Stage")
        self.setWindowIcon(QIcon("resources/A5-favicon.png"))
        self.setFixedSize(400, 520)
        layout = QVBoxLayout(self)

        # Load the pickled model
        self.model = self.load_model()

        # Text for Construction Stage page
        construction_text = QTextEdit(self)
        construction_text.setPlainText(
            """Provide the following information to estimate emissions:
            
1. Select machinery.
2. Enter quantity.
3. Fuel consumption rate is automatically assigned based on equipment selected (litres/h).
4. Enter hours of operation (h).
5. Carbon emission factor is automatically assigned based on equipment selected (kgCO2/kg).
            """)
        construction_text.setReadOnly(True)
        layout.addWidget(construction_text)

        # Create the form layout
        form_layout = QFormLayout()

        # Create widgets for the form
        self.machinery_combo = QComboBox()
        self.machinery_list = [
            'Bulldozer', 'Crane', 'Concrete mixer', 'Rock crusher', 'Concrete pump',
            'Air compressor', 'Road roller', 'Power buggy', 'Floor grinder', 'Crusher'
        ]
        self.machinery_combo.addItems(self.machinery_list)
        self.machinery_combo.currentIndexChanged.connect(self.update_fuel_and_emission_factors)

        self.quantity_input = QLineEdit()
        self.quantity_input.setPlaceholderText('Enter quantity')

        self.fuel_consumption_input = QLineEdit()
        self.fuel_consumption_input.setReadOnly(True)

        self.hours_input = QLineEdit()
        self.hours_input.setPlaceholderText('Enter hours of operation')

        self.carbon_factor_input = QLineEdit()
        self.carbon_factor_input.setReadOnly(True)

        # Add form widgets to the form layout
        form_layout.addRow('Machinery:', self.machinery_combo)
        form_layout.addRow('Quantity:', self.quantity_input)
        form_layout.addRow('Fuel Consumption Rate:', self.fuel_consumption_input)
        form_layout.addRow('Hours of Operation:', self.hours_input)
        form_layout.addRow('Carbon Emission Factor:', self.carbon_factor_input)

        # Create a button and connect it to the predict method
        predict_button = QPushButton('Predict Total Carbon Emission')
        predict_button.clicked.connect(self.predict)
        form_layout.addRow(predict_button)

        # Add the form layout to the main layout
        layout.addLayout(form_layout)

        # Label for displaying results
        self.result_label = QLabel("", self)
        layout.addWidget(self.result_label)

        # Initialize the fuel and emission factors
        self.update_fuel_and_emission_factors()

    def load_model(self):
        # Load the pickled model from file
        model_path = 'models/Gradient-Boosting-A5.pkl'  # Path to your model
        with open(model_path, 'rb') as file:
            model = pickle.load(file)
        return model

    def update_fuel_and_emission_factors(self):
        # Fuel consumption rates and emission factors based on machinery
        machinery_factors = {
            'Bulldozer': (20, 1.5),
            'Crane': (30, 2),
            'Concrete mixer': (18, 1.6),
            'Rock crusher': (40, 2.5),
            'Concrete pump': (32, 2.3),
            'Air compressor': (18, 1.6),
            'Road roller': (25, 1.9),
            'Power buggy': (15, 1.4),
            'Floor grinder': (40, 2.5),
            'Crusher': (50, 2.8)
        }
        selected_machinery = self.machinery_combo.currentText()
        fuel_consumption, carbon_factor = machinery_factors.get(selected_machinery, ("", ""))

        self.fuel_consumption_input.setText(str(fuel_consumption))
        self.carbon_factor_input.setText(str(carbon_factor))

    def predict(self):
        # Get the input values
        machinery = self.machinery_combo.currentText()
        quantity = self.quantity_input.text()
        fuel_consumption = self.fuel_consumption_input.text()
        hours = self.hours_input.text()
        carbon_factor = self.carbon_factor_input.text()

        if not quantity or not hours:
            QMessageBox.warning(self, "Input Error", "Please provide all required inputs.")
            return

        try:
            quantity = float(quantity)
            fuel_consumption = float(fuel_consumption)
            hours = float(hours)
            carbon_factor = float(carbon_factor)
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Quantity and Hours of Operation must be numeric.")
            return

        # Convert categorical input to numerical
        machinery_mapping = {mach: idx for idx, mach in enumerate(self.machinery_list)}
        machinery_num = machinery_mapping.get(machinery, -1)

        if machinery_num == -1:
            QMessageBox.warning(self, "Input Error", "Invalid machinery type selected.")
            return

        # Prepare the feature vector
        features = pd.DataFrame({
            'Machinery': [machinery_num],
            'Quantity': [quantity],
            'Fuel_consumption_rate': [fuel_consumption],
            'Hours_of_operation': [hours],
            'Carbon_emission_factor': [carbon_factor]
        })

        # Perform prediction
        try:
            prediction = self.model.predict(features)[0]
            self.result_label.setText(f"Predicted Total Carbon Emission: {prediction:.2f} kgCO2e")
        except Exception as e:
            QMessageBox.critical(self, "Prediction Error", f"An error occurred during prediction: {str(e)}")
