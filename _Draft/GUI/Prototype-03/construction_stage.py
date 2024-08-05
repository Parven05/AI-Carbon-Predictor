from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QFormLayout, QLineEdit, QComboBox, QPushButton

class ConstructionStageWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Construction Stage")
        self.setGeometry(200, 200, 400, 350)
        layout = QVBoxLayout(self)

        # Text for Construction Stage page
        construction_text = QLabel(
            """Provide the following information to estimate emissions for the construction stage:
            
1. Select construction activity.
2. Enter number of workers.
3. Enter hours of work.
4. Enter equipment fuel consumption.
5. Enter carbon emission factor.
            """, self)
        layout.addWidget(construction_text)

        # Create the form layout
        form_layout = QFormLayout()

        # Create widgets for the form
        self.activity_combo = QComboBox()
        self.activity_combo.addItems(['Excavation', 'Concrete Pouring', 'Roof Installation'])  # Example items

        self.workers_input = QLineEdit()
        self.workers_input.setPlaceholderText('Enter number of workers')

        self.hours_input = QLineEdit()
        self.hours_input.setPlaceholderText('Enter hours of work')

        self.fuel_consumption_input = QLineEdit()
        self.fuel_consumption_input.setPlaceholderText('Enter equipment fuel consumption')

        self.carbon_factor_input = QLineEdit()
        self.carbon_factor_input.setPlaceholderText('Enter carbon emission factor')

        # Add form widgets to the form layout
        form_layout.addRow('Construction Activity:', self.activity_combo)
        form_layout.addRow('Number of Workers:', self.workers_input)
        form_layout.addRow('Hours of Work:', self.hours_input)
        form_layout.addRow('Equipment Fuel Consumption:', self.fuel_consumption_input)
        form_layout.addRow('Carbon Emission Factor:', self.carbon_factor_input)

        # Create a button
        predict_button = QPushButton('Predict')
        form_layout.addRow(predict_button)

        # Add the form layout to the main layout
        layout.addLayout(form_layout)
