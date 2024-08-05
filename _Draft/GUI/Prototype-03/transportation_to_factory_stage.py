import pickle
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QFormLayout, QLineEdit, QComboBox, QPushButton, QMessageBox
import pandas as pd

class TransportationToFactoryStageWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Transportation to Factory Stage")
        self.setGeometry(200, 200, 400, 350)
        layout = QVBoxLayout(self)

        # Load the pickled model
        self.model = self.load_model()

        # Text for Transportation to Factory Stage page
        transportation_text = QLabel(
            """Provide the following information to estimate emissions for the transportation to factory stage:
            
1. Select material type.
2. Enter mass used.
3. Enter distance traveled.
4. Enter fuel consumption.
5. Enter carbon emission factor.
            """, self)
        layout.addWidget(transportation_text)

        # Create the form layout
        form_layout = QFormLayout()

        # Create widgets for the form
        self.material_combo = QComboBox()
        self.material_combo.addItems(['Wood', 'Steel', 'Concrete'])  # Example items

        self.mass_input = QLineEdit()
        self.mass_input.setPlaceholderText('Enter mass used')

        self.distance_input = QLineEdit()
        self.distance_input.setPlaceholderText('Enter distance traveled')

        self.fuel_consumption_input = QLineEdit()
        self.fuel_consumption_input.setPlaceholderText('Enter fuel consumption')

        self.carbon_factor_input = QLineEdit()
        self.carbon_factor_input.setPlaceholderText('Enter carbon emission factor')

        # Add form widgets to the form layout
        form_layout.addRow('Material Type:', self.material_combo)
        form_layout.addRow('Mass Used:', self.mass_input)
        form_layout.addRow('Distance Traveled:', self.distance_input)
        form_layout.addRow('Fuel Consumption:', self.fuel_consumption_input)
        form_layout.addRow('Carbon Emission Factor:', self.carbon_factor_input)

        # Create a button
        predict_button = QPushButton('Predict')
        predict_button.clicked.connect(self.predict)  # Connect button to predict method
        form_layout.addRow(predict_button)

        # Add the form layout to the main layout
        layout.addLayout(form_layout)

        # Label for displaying results
        self.result_label = QLabel("", self)
        layout.addWidget(self.result_label)

    def load_model(self):
        # Load the pickled model from file
        model_path = 'models/Gradient-Boosting-A2.pkl'  # Path to your model
        with open(model_path, 'rb') as file:
            model = pickle.load(file)
        return model

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
        material_mapping = {'Wood': 0, 'Steel': 1, 'Concrete': 2}
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
            self.result_label.setText(f"Predicted Emission: {prediction:.2f}")
        except Exception as e:
            QMessageBox.critical(self, "Prediction Error", f"An error occurred during prediction: {str(e)}")
