import pickle
from PySide6.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QFormLayout, QLineEdit, QComboBox, QPushButton, QMessageBox, QLabel
from PySide6.QtGui import QIcon
import pandas as pd
from central_data_store import PredictionStore

class TransportationToSiteStageWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Transportation to Site Stage")
        self.setWindowIcon(QIcon("resources/A4-favicon.png"))
        self.setFixedSize(400, 520)
        layout = QVBoxLayout(self)

        # Load the pickled model
        self.model = self.load_model()

        # Text for Transportation to Site Stage page
        transportation_text = QTextEdit(self)
        transportation_text.setPlainText(
            """Provide the following information to estimate emissions:
            
1. Select material type.
2. Enter mass used (kg).
3. Enter distance traveled (km).
4. Fuel consumption rate is automatically assigned based on equipment selected (litres/h).
5. Carbon emission factor is automatically assigned based on equipment selected (kgCO2/kg).
            """)
        transportation_text.setReadOnly(True)
        layout.addWidget(transportation_text)

        # Create the form layout
        form_layout = QFormLayout()

        # Create widgets for the form
        self.material_combo = QComboBox()
        self.materials = [
            'AAC blocks', 'Aluminium studs', 'Cement board', 'Door frame',
            'Duct tape', 'Fiberboard', 'Metal siding', 'Resins',
            'Stainless steel', 'Stone wool'
        ]
        self.material_combo.addItems(self.materials)
        self.material_combo.currentIndexChanged.connect(self.update_carbon_factor)

        self.mass_input = QLineEdit()
        self.mass_input.setPlaceholderText('Enter mass used (kg)')

        self.distance_input = QLineEdit()
        self.distance_input.setPlaceholderText('Enter distance traveled (km)')

        self.fuel_consumption_input = QLineEdit()
        self.fuel_consumption_input.setText('0.4')
        self.fuel_consumption_input.setReadOnly(True)  # Make this field read-only

        self.carbon_factor_input = QLineEdit()
        self.carbon_factor_input.setReadOnly(True)  # Make this field read-only

        # Add form widgets to the form layout
        form_layout.addRow('Material Type:', self.material_combo)
        form_layout.addRow('Mass Used:', self.mass_input)
        form_layout.addRow('Distance Traveled:', self.distance_input)
        form_layout.addRow('Fuel Consumption Rate:', self.fuel_consumption_input)
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

        # Update carbon factor based on initial selection
        self.update_carbon_factor()

    def load_model(self):
        # Load the pickled model from file
        model_path = 'models/Gradient-Boosting-A4.pkl'  # Path to your model
        with open(model_path, 'rb') as file:
            model = pickle.load(file)
        return model

    def update_carbon_factor(self):
        # Update the carbon emission factor based on selected material
        material_factors = {
            'AAC blocks': 0.6,
            'Aluminium studs': 11,
            'Cement board': 0.7,
            'Door frame': 0.6,
            'Duct tape': 0.3,
            'Fiberboard': 0.6,
            'Metal siding': 2.5,
            'Resins': 7.5,
            'Stainless steel': 4,
            'Stone wool': 3
        }
        selected_material = self.material_combo.currentText()
        carbon_factor = material_factors.get(selected_material, "")
        self.carbon_factor_input.setText(str(carbon_factor))

    def predict(self):
        # Get the input values
        material = self.material_combo.currentText()
        mass = self.mass_input.text()
        distance_traveled = self.distance_input.text()
        fuel_consumption = self.fuel_consumption_input.text()  # This will always be 0.4
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
            'Materials': [material_num],
            'Mass_used': [mass],
            'Distance_traveled': [distance_traveled],
            'Fuel_consumption_rate': [fuel_consumption],
            'Carbon_emission_factor': [carbon_factor]
        })

        # Perform prediction
        try:
            prediction = self.model.predict(features)[0]
            self.predicted_emission = prediction  # Store the prediction
            
            store = PredictionStore()
            store.set_prediction('transportation_to_site', prediction)

            self.result_label.setText(f"Predicted Total Carbon Emission: {prediction:.2f} kgCO2e")
        except Exception as e:
            QMessageBox.critical(self, "Prediction Error", f"An error occurred during prediction: {str(e)}")

    def get_prediction(self):
        return getattr(self, 'predicted_emission', 0)