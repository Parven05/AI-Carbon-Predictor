import pickle
from PySide6.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QFormLayout, QLineEdit, QComboBox, QPushButton, QMessageBox, QLabel
from PySide6.QtGui import QIcon
import pandas as pd

class ManufacturingStageWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Manufacturing Stage")
        self.setWindowIcon(QIcon("resources/A3-favicon.png"))
        self.setFixedSize(400, 520)
        layout = QVBoxLayout(self)

        # Load the pickled model
        self.model = self.load_model()

        # Text for Manufacturing Stage page
        manufacturing_text = QTextEdit(self)
        manufacturing_text.setPlainText(
            """Provide the following information to estimate emissions:
            
1. Select manufacturing equipment/machinery.
2. Enter quantity.
3. Fuel consumption rate is automatically assigned based on equipment selected (litres/h).
4. Enter hours of operation (h).
5. Carbon emission factor is automatically assigned based on equipment selected (kgCO2/kg).
            """)
        manufacturing_text.setReadOnly(True)
        layout.addWidget(manufacturing_text)

        # Create the form layout
        form_layout = QFormLayout()

        # Create widgets for the form
        self.equipment_combo = QComboBox()
        self.equipment_types = {
            'Welding machine': 15,
            'Electric furnace': 50,
            'Generator': 10,
            'Forklift': 4,
            'Laser cutter': 8,
            'Hydraulic press': 10,
            'Bending machine': 7,
            'Extruder': 25,
            'Drill press': 2,
            'Sandblaster': 10
        }
        self.equipment_combo.addItems(self.equipment_types.keys())
        self.equipment_combo.currentIndexChanged.connect(self.update_fuel_consumption)

        self.quantity_input = QLineEdit()
        self.quantity_input.setPlaceholderText('Enter quantity')

        self.fuel_consumption_input = QLineEdit()
        self.fuel_consumption_input.setPlaceholderText('Fuel consumption (litres/h)')
        self.fuel_consumption_input.setReadOnly(True)  # Set fuel consumption as read-only

        self.hours_input = QLineEdit()
        self.hours_input.setPlaceholderText('Enter hours of operation')

        self.carbon_factor_input = QLineEdit()
        self.carbon_factor_input.setText('0.5')
        self.carbon_factor_input.setReadOnly(True)  # Set carbon emission factor as read-only

        # Add form widgets to the form layout
        form_layout.addRow('Manufacturing Equipment:', self.equipment_combo)
        form_layout.addRow('Quantity:', self.quantity_input)
        form_layout.addRow('Fuel Consumption Rate:', self.fuel_consumption_input)
        form_layout.addRow('Hours of Operation:', self.hours_input)
        form_layout.addRow('Carbon Emission Factor:', self.carbon_factor_input)

        # Create a button and connect it to the predict method
        predict_button = QPushButton('Predict Total Carbon Emission')
        predict_button.clicked.connect(self.predict)  # Connect button to predict method
        form_layout.addRow(predict_button)

        # Add the form layout to the main layout
        layout.addLayout(form_layout)

        # Label for displaying results
        self.result_label = QLabel("", self)
        layout.addWidget(self.result_label)

        # Update fuel consumption based on initial selection
        self.update_fuel_consumption()

    def load_model(self):
        # Load the pickled model from file
        model_path = 'models/Gradient-Boosting-A3.pkl'  # Path to your model
        with open(model_path, 'rb') as file:
            model = pickle.load(file)
        return model

    def update_fuel_consumption(self):
        # Update the fuel consumption rate based on selected equipment
        selected_equipment = self.equipment_combo.currentText()
        fuel_consumption = self.equipment_types.get(selected_equipment, "")
        self.fuel_consumption_input.setText(str(fuel_consumption))

    def predict(self):
        # Get the input values
        equipment = self.equipment_combo.currentText()
        quantity = self.quantity_input.text()
        fuel_consumption = self.fuel_consumption_input.text()
        hours = self.hours_input.text()
        carbon_factor = self.carbon_factor_input.text()

        if not quantity or not hours or not carbon_factor:
            QMessageBox.warning(self, "Input Error", "Please provide all numeric inputs.")
            return

        try:
            quantity = float(quantity)
            fuel_consumption = float(fuel_consumption)
            hours = float(hours)
            carbon_factor = float(carbon_factor)
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Quantity, Fuel Consumption, Hours of Operation, and Carbon Emission Factor must be numeric.")
            return

        # Convert categorical input to numerical
        equipment_mapping = {equip: idx for idx, equip in enumerate(self.equipment_types.keys())}
        equipment_num = equipment_mapping.get(equipment, -1)

        if equipment_num == -1:
            QMessageBox.warning(self, "Input Error", "Invalid equipment type selected.")
            return

        # Prepare the feature vector
        features = pd.DataFrame({
            'Manufacturing_equipment': [equipment_num],
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
