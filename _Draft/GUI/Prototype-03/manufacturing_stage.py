from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QFormLayout, QLineEdit, QComboBox, QPushButton

class ManufacturingStageWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Manufacturing Stage")
        self.setGeometry(200, 200, 400, 350)
        layout = QVBoxLayout(self)

        # Text for Manufacturing Stage page
        manufacturing_text = QLabel(
            """Provide the following information to estimate emissions for the manufacturing stage:
            
1. Select manufacturing equipment/machinery.
2. Enter quantity.
3. Enter fuel consumption rate.
4. Enter hours of operation.
5. Enter carbon emission factor.
            """, self)
        layout.addWidget(manufacturing_text)

        # Create the form layout
        form_layout = QFormLayout()

        # Create widgets for the form
        self.equipment_combo = QComboBox()
        self.equipment_combo.addItems(['Excavator', 'Bulldozer', 'Crane'])  # Example items

        self.quantity_input = QLineEdit()
        self.quantity_input.setPlaceholderText('Enter quantity')

        self.fuel_consumption_input = QLineEdit()
        self.fuel_consumption_input.setPlaceholderText('Enter fuel consumption')

        self.hours_input = QLineEdit()
        self.hours_input.setPlaceholderText('Enter hours of operation')

        self.carbon_factor_input = QLineEdit()
        self.carbon_factor_input.setPlaceholderText('Enter carbon emission factor')

        # Add form widgets to the form layout
        form_layout.addRow('Manufacturing Equipment:', self.equipment_combo)
        form_layout.addRow('Quantity:', self.quantity_input)
        form_layout.addRow('Fuel Consumption Rate:', self.fuel_consumption_input)
        form_layout.addRow('Hours of Operation:', self.hours_input)
        form_layout.addRow('Carbon Emission Factor:', self.carbon_factor_input)

        # Create a button
        predict_button = QPushButton('Predict')
        form_layout.addRow(predict_button)

        # Add the form layout to the main layout
        layout.addLayout(form_layout)
