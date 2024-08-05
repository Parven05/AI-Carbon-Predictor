from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QFormLayout, QLineEdit, QComboBox, QPushButton

class TransportationToSiteStageWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Transportation to Site Stage")
        self.setGeometry(200, 200, 400, 350)
        layout = QVBoxLayout(self)

        # Text for Transportation to Site Stage page
        transportation_text = QLabel(
            """Provide the following information to estimate emissions for the transportation to site stage:
            
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
        form_layout.addRow(predict_button)

        # Add the form layout to the main layout
        layout.addLayout(form_layout)
