from PySide6.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QFormLayout, QLineEdit, QPushButton, QMessageBox, QLabel
from PySide6.QtGui import QIcon
from central_data_store import PredictionStore

class TotalCarbonEmissionWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Total Carbon Emission")
        self.setWindowIcon(QIcon("resources/total-favicon.png"))
        self.setFixedSize(400, 540)
        layout = QVBoxLayout(self)

        # Text for Total Carbon Emission page
        emission_text = QTextEdit(self)
        emission_text.setPlainText(
            """Provide the following information to estimate emissions:

1. Upro, represents total carbon emission of production stage.
2. Uttf, represents total carbon emission of transportation to factory stage.
3. Umat, represents total carbon emission of manufacturing stage.
4. Utts, represents total carbon emission of transportation to site stage.
5. Ucon, represents total carbon emission of construction stage.
            """)
        emission_text.setReadOnly(True)
        layout.addWidget(emission_text)

        # Create the form layout
        form_layout = QFormLayout()

        # Create widgets for the form
        self.production_input = QLineEdit()
        self.production_input.setReadOnly(True)

        self.transportation_to_factory_input = QLineEdit()
        self.transportation_to_factory_input.setReadOnly(True)

        self.manufacturing_input = QLineEdit()
        self.manufacturing_input.setReadOnly(True)

        self.transportation_to_site_input = QLineEdit()
        self.transportation_to_site_input.setReadOnly(True)

        self.construction_input = QLineEdit()
        self.construction_input.setReadOnly(True)

        # Add form widgets to the form layout
        form_layout.addRow('Upro:', self.production_input)
        form_layout.addRow('Uttf:', self.transportation_to_factory_input)
        form_layout.addRow('Umat:', self.manufacturing_input)
        form_layout.addRow('Utts:', self.transportation_to_site_input)
        form_layout.addRow('Ucon:', self.construction_input)

        # Create a button and connect it to the calculate method
        calculate_button = QPushButton('Calculate Total Carbon Emission')
        calculate_button.clicked.connect(self.calculate)
        form_layout.addRow(calculate_button)

        # Add the form layout to the main layout
        layout.addLayout(form_layout)

        # Label for displaying results
        self.result_label = QLabel("", self)
        layout.addWidget(self.result_label)

        # Initialize input fields
        self.update_predictions()

    def update_predictions(self):
        """Update the input fields with current emissions values from the central data store."""
        try:
            store = PredictionStore()
            self.production_input.setText(f"{store.get_prediction('production'):.2f} kgCO2e")
            self.transportation_to_factory_input.setText(f"{store.get_prediction('transportation_to_factory'):.2f} kgCO2e")
            self.manufacturing_input.setText(f"{store.get_prediction('manufacturing'):.2f} kgCO2e")
            self.transportation_to_site_input.setText(f"{store.get_prediction('transportation_to_site'):.2f} kgCO2e")
            self.construction_input.setText(f"{store.get_prediction('construction'):.2f} kgCO2e")
        except Exception as e:
            QMessageBox.critical(self, "Initialization Error", f"An error occurred while updating predictions: {str(e)}")

    def calculate(self):
        """Calculate the total carbon emission from all stages."""
        try:
            # Retrieve predictions from the central data store
            store = PredictionStore()
            production_emission = store.get_prediction('production')
            transportation_to_factory_emission = store.get_prediction('transportation_to_factory')
            manufacturing_emission = store.get_prediction('manufacturing')
            transportation_to_site_emission = store.get_prediction('transportation_to_site')
            construction_emission = store.get_prediction('construction')

            # Calculate total emission
            total_emission = (production_emission + transportation_to_factory_emission +
                              manufacturing_emission + transportation_to_site_emission +
                              construction_emission)

            # Update the result label
            self.result_label.setText(f"Calculated Total Carbon Emission: {total_emission:.2f} kgCO2e")
        except ValueError as e:
            QMessageBox.critical(self, "Calculation Error", f"An error occurred during calculation: {str(e)}")
