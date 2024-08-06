from scripts.packages import QDialog, QVBoxLayout, QLabel, QFormLayout, QLineEdit, QPushButton, QTextEdit, QMessageBox, QIcon
from scripts.textStorage import load_text
from scripts.data import PredictionStore

class TotalWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.update_predictions()

    def setup_ui(self):
        self.setWindowTitle("Total Carbon Emission")
        self.setWindowIcon(QIcon("resources/images/total-favicon.png"))
        self.setFixedSize(400, 540)

        # Main layout
        layout = QVBoxLayout(self)

        # Add instruction text
        self.emission_text = self.create_text_edit("resources/text/total.txt")
        layout.addWidget(self.emission_text)

        # Add form layout
        self.form_layout = self.create_form_layout()
        layout.addLayout(self.form_layout)

        # Result label
        self.result_label = QLabel("", self)
        layout.addWidget(self.result_label)

    def create_text_edit(self, file_path):
        text_edit = QTextEdit(self)
        text_edit.setPlainText(load_text(file_path))
        text_edit.setReadOnly(True)
        return text_edit

    def create_form_layout(self):
        form_layout = QFormLayout()

        # Create input fields for various stages
        self.production_input = self.create_read_only_input()
        self.transportation_to_factory_input = self.create_read_only_input()
        self.manufacturing_input = self.create_read_only_input()
        self.transportation_to_site_input = self.create_read_only_input()
        self.construction_input = self.create_read_only_input()

        # Add input fields to the form layout
        form_layout.addRow('Upro:', self.production_input)
        form_layout.addRow('Uttf:', self.transportation_to_factory_input)
        form_layout.addRow('Umat:', self.manufacturing_input)
        form_layout.addRow('Utts:', self.transportation_to_site_input)
        form_layout.addRow('Ucon:', self.construction_input)

        # Create and add the calculate button
        calculate_button = QPushButton('Calculate Total Carbon Emission')
        calculate_button.clicked.connect(self.calculate_total_emission)
        form_layout.addRow(calculate_button)

        return form_layout

    def create_read_only_input(self):
        input_field = QLineEdit(readOnly=True)
        return input_field

    def update_predictions(self):
        try:
            store = PredictionStore()
            self.production_input.setText(self.format_prediction(store.get_prediction('production')))
            self.transportation_to_factory_input.setText(self.format_prediction(store.get_prediction('transportation_to_factory')))
            self.manufacturing_input.setText(self.format_prediction(store.get_prediction('manufacturing')))
            self.transportation_to_site_input.setText(self.format_prediction(store.get_prediction('transportation_to_site')))
            self.construction_input.setText(self.format_prediction(store.get_prediction('construction')))
        except Exception as e:
            QMessageBox.critical(self, "Initialization Error", f"An error occurred while updating predictions: {str(e)}")

    def format_prediction(self, prediction):
        return f"{prediction:.2f} kgCO2e"

    def calculate_total_emission(self):
        try:
            store = PredictionStore()
            total_emission = sum([
                store.get_prediction('production'),
                store.get_prediction('transportation_to_factory'),
                store.get_prediction('manufacturing'),
                store.get_prediction('transportation_to_site'),
                store.get_prediction('construction')
            ])

            self.result_label.setText(f"Calculated Total Carbon Emission: {total_emission:.2f} kgCO2e")
        except Exception as e:
            QMessageBox.critical(self, "Calculation Error", f"An error occurred during calculation: {str(e)}")
