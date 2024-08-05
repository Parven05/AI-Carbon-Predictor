import pickle
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QFormLayout, QLineEdit, QComboBox, QPushButton, QMessageBox
from PySide6.QtGui import QIcon
import pandas as pd

class TransportationToFactoryStageWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Transportation to Factory Stage")
        self.setWindowIcon(QIcon("resources/A2-favicon.png"))
        self.setFixedSize(400, 500)
        layout = QVBoxLayout(self)

        # Load the pickled model
        self.model = self.load_model()

        # Text for Transportation to Factory Stage page
        transportation_text = QLabel(
            """Provide the following information to estimate emissions:
            
1. Select Raw material type.
2. Enter mass used (kg) | Recommended: 50 - 2000 (kg).
3. Enter distance traveled (km) | Recommended: 100 - 500 (km).
4. Fuel consumption is automatically set to 0.4 litres/km.
5. Carbon emission factor is automatically assigned based on material selected.
            """, self)
        layout.addWidget(transportation_text)

        # Create the form layout
        form_layout = QFormLayout()

        # Create widgets for the form
        self.material_combo = QComboBox()
        self.materials = ['Cement', 'Concrete', 'Steel', 'Asphalt', 'Bricks', 'Glass', 'Wood', 'Aluminium', 'Stone', 'Plastics']
        self.material_combo.addItems(self.materials)
        self.material_combo.currentIndexChanged.connect(self.update_carbon_factor)

        self.carbon_factors = {
            'Cement': 0.9,
            'Concrete': 0.3,
            'Steel': 1.8,
            'Asphalt': 0.1,
            'Bricks': 0.5,
            'Glass': 0.8,
            'Wood': 0.2,
            'Aluminium': 11.0,
            'Stone': 0.4,
            'Plastics': 6.0
        }

        self.mass_input = QLineEdit()
        self.mass_input.setPlaceholderText('Enter mass used (kg)')

        self.distance_input = QLineEdit()
        self.distance_input.setPlaceholderText('Enter distance traveled (km)')

        self.fuel_consumption_input = QLineEdit()
        self.fuel_consumption_input.setText('0.4')
        self.fuel_consumption_input.setReadOnly(True)  # Set fuel consumption as read-only

        self.carbon_factor_input = QLineEdit()
        self.carbon_factor_input.setPlaceholderText('Emission factor (kgCO2/l)')
        self.carbon_factor_input.setReadOnly(True)  # Carbon emission factor is read-only

        # Add form widgets to the form layout
        form_layout.addRow('Material Type:', self.material_combo)
        form_layout.addRow('Mass Used:', self.mass_input)
        form_layout.addRow('Distance Traveled:', self.distance_input)
        form_layout.addRow('Fuel Consumption Rate:', self.fuel_consumption_input)
        form_layout.addRow('Carbon Emission Factor:', self.carbon_factor_input)

        # Create a button
        predict_button = QPushButton('Predict Total Carbon Emission')
        predict_button.clicked.connect(self.predict)  # Connect button to predict method
        form_layout.addRow(predict_button)

        # Add the form layout to the main layout
        layout.addLayout(form_layout)

        # Label for displaying results
        self.result_label = QLabel("", self)
        layout.addWidget(self.result_label)

        # Update carbon factor based on initial selection
        self.update_carbon_factor()

    def load_model(self):
        # Load the pickled model from file
        model_path = 'models/Gradient-Boosting-A2.pkl'  # Path to your model
        with open(model_path, 'rb') as file:
            model = pickle.load(file)
        return model

    def update_carbon_factor(self):
        # Update the carbon emission factor based on selected material
        selected_material = self.material_combo.currentText()
        carbon_factor = self.carbon_factors.get(selected_material, "")
        self.carbon_factor_input.setText(str(carbon_factor))

    def predict(self):
        # Get the input values
        material = self.material_combo.currentText()
        mass = self.mass_input.text()
        distance_traveled = self.distance_input.text()
        fuel_consumption = self.fuel_consumption_input.text()
        carbon_factor = self.carbon_factor_input.text()

        if not mass or not distance_traveled or not fuel_consumption or not carbon_factor:
            QMessageBox.warning(self, "Input Error", "Please provide all numeric inputs.")
            return

        try:
            mass = float(mass)
            distance_traveled = float(distance_traveled)
            fuel_consumption = float(fuel_consumption)
            carbon_factor = float(carbon_factor)
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Mass, Distance, Fuel Consumption, and Carbon Emission Factor must be numeric.")
            return

        # Convert categorical input to numerical
        material_mapping = {mat: idx for idx, mat in enumerate(self.materials)}
        material_num = material_mapping.get(material, -1)

        if material_num == -1:
            QMessageBox.warning(self, "Input Error", "Invalid material type selected.")
            return

        # Prepare the feature vector
        features = pd.DataFrame({
            'Raw_material': [material_num],
            'Mass_used': [mass],
            'Distance_traveled': [distance_traveled],
            'Fuel_consumption_rate': [fuel_consumption],
            'Carbon_emission_factor': [carbon_factor]
        })

        # Perform prediction
        try:
            prediction = self.model.predict(features)[0]
            self.result_label.setText(f"Predicted Total Carbon Emission: {prediction:.2f} kgCO2e")
        except Exception as e:
            QMessageBox.critical(self, "Prediction Error", f"An error occurred during prediction: {str(e)}")
