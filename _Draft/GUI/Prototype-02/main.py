import sys
import pickle
import numpy as np
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton,
    QHBoxLayout, QFrame, QSizePolicy, QComboBox, QLineEdit, QMessageBox
)
from PySide6.QtGui import QFont, QFontDatabase, QIcon, QPixmap
from PySide6.QtCore import Qt

# Define the color palette
color_palette = {
    'green': '#92c730',
    'orange': '#f79862',
    'brown': '#cd7f32',
    'text': '#000000',
    'background': '#f5f5f5',  # Light background color
    'frame': '#e0e0e0',       # Light gray for frames and borders
    'button': '#f79862'       # Orange for buttons
}

# Function to prepare features
def prepare_features(categorical_value, numeric_features, encoding_map):
    feature_vector = np.zeros(total_features)  # Create a vector with total_features

    if categorical_value in encoding_map:
        categorical_index = encoding_map[categorical_value]
        feature_vector[categorical_index] = 1  # Set the categorical feature

    if len(numeric_features) == 2:
        feature_vector[1] = numeric_features[0]  # Set the first numeric feature
        feature_vector[2] = numeric_features[1]  # Set the second numeric feature

    return feature_vector

# Class to handle the model
class ModelHandler:
    def __init__(self, model_path, total_features):
        self.total_features = total_features
        self.model = self.load_model(model_path)
        
    def load_model(self, model_path):
        with open(model_path, 'rb') as model_file:
            return pickle.load(model_file)
        
    def predict(self, categorical_value, numeric_features, encoding_map):
        feature_vector = prepare_features(categorical_value, numeric_features, encoding_map, self.total_features)
        feature_vector = np.array(feature_vector).reshape(1, -1)  # Convert to NumPy array and reshape
        return self.model.predict(feature_vector)

# Basic GUI to show model is loaded
class MainWindow(QMainWindow):
    def __init__(self, initial_model_path):
        super().__init__()
        
        self.model_handler = ModelHandler(initial_model_path, self.total_features)
        
        self.setWindowTitle("Smart Build Co2 Predictor")
        self.setGeometry(100, 100, 800, 400)
        self.setWindowIcon(QIcon("puo_logo.png"))

        # Load a custom font
        font_id = QFontDatabase.addApplicationFont('path/to/your/font.ttf')
        font_families = QFontDatabase.applicationFontFamilies(font_id)

        if font_families:
            font_family = font_families[0]
        else:
            font_family = "Roboto"  # Fallback to a default font if custom font fails

        font = QFont(font_family, 12)  # Set the font and size
        self.setFont(font)

        # Central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
        central_widget.setStyleSheet(f"background-color: {color_palette['background']};")
        
        # Create a horizontal layout for the top menu
        top_menu_layout = QHBoxLayout()
        top_menu_layout.setSpacing(10)
        
        # Define menu items
        menu_items = [
            ("Welcome", self.show_welcome_message),
            ("Production Stage", self.show_production_stage_page),
            ("Transportation to Factory", lambda: self.load_model('./Gradient-Boosting-A2.pkcls')),
            ("Manufacturing", lambda: self.load_model('./Gradient-Boosting-A3.pkcls')),
            ("Transportation to Site", lambda: self.load_model('./Gradient-Boosting-A4.pkcls')),
            ("Construction", lambda: self.load_model('./Gradient-Boosting-A5.pkcls'))
        ]
        
        # Create buttons for menu items with consistent sizing
        button_size_policy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        for text, action in menu_items:
            button = QPushButton(text, self)
            button.clicked.connect(action)
            button.setSizePolicy(button_size_policy)
            button.setStyleSheet(f"""
                background-color: {color_palette['button']};
                color: {color_palette['text']};
                border: 1px solid {color_palette['frame']};
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            """)
            top_menu_layout.addWidget(button)
        
        # Add top menu layout to the main layout
        main_layout.addLayout(top_menu_layout)

        # Add a horizontal line for separation
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet(f"color: {color_palette['brown']};")
        main_layout.addWidget(separator)
        
        # Create and add the central content
        self.central_content_layout = QVBoxLayout()
        self.central_content_layout.setSpacing(10)
        main_layout.addLayout(self.central_content_layout)
        
        # Show welcome page by default
        self.show_welcome_message()

    def show_welcome_message(self):
        # Clear the central content layout
        self.clear_central_content()

        # Create a horizontal layout for the welcome page
        welcome_layout = QHBoxLayout()
        welcome_layout.setContentsMargins(50, 50, 50, 50)  # Add margins for spacing
        
        # Image on the left
        self.image_label = QLabel(self)
        self.image_pixmap = QPixmap('logo.png')  # Replace with your image path
        self.image_pixmap = self.image_pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio, Qt.SmoothTransformation)  # Resize with smooth transformation
        self.image_label.setPixmap(self.image_pixmap)
        self.image_label.setAlignment(Qt.AlignCenter)
        welcome_layout.addWidget(self.image_label)
        
        # Spacer to push the text to the right
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        welcome_layout.addWidget(spacer)
        
        # Text on the right
        self.label = QLabel("Welcome to the Model Loading GUI.\n\nUse the buttons above to load different models or view information about the GUI.", self)
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)  # Left-align text and center vertically
        self.label.setStyleSheet(f"color: {color_palette['text']};")  # Set text color
        welcome_layout.addWidget(self.label)
        
        # Add the welcome layout to the central content layout
        self.central_content_layout.addLayout(welcome_layout)

    def show_production_stage_page(self):
        # Clear the central content layout
        self.clear_central_content()

        # Create a horizontal layout for the production stage page
        production_layout = QHBoxLayout()
        production_layout.setContentsMargins(50, 50, 50, 50)  # Add margins for spacing

        # Image on the left
        self.image_label = QLabel(self)
        self.image_pixmap = QPixmap('logo.png')  # Replace with your image path
        self.image_pixmap = self.image_pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio, Qt.SmoothTransformation)  # Resize with smooth transformation
        self.image_label.setPixmap(self.image_pixmap)
        self.image_label.setAlignment(Qt.AlignCenter)
        production_layout.addWidget(self.image_label)

        # Spacer to push the input box to the right
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        production_layout.addWidget(spacer)

        # Create a QFrame to contain the input fields
        input_frame = QFrame(self)
        input_frame.setFrameShape(QFrame.StyledPanel)  # Set the frame shape to a styled panel
        input_frame.setStyleSheet(f"""
            background-color: {color_palette['background']};
            border: 1px solid {color_palette['frame']};
            border-radius: 10px;
            padding: 20px;
        """)  # Set background color and border style
        input_layout = QVBoxLayout(input_frame)
        input_layout.setSpacing(10)

        # Explanatory text
        explanation_text = QLabel("Enter the mass and carbon emission factor for the production stage.", input_frame)
        explanation_text.setStyleSheet(f"color: {color_palette['text']};")
        input_layout.addWidget(explanation_text)

        # Searchable dropdown (QComboBox)
        self.material_dropdown = QComboBox(input_frame)
        self.material_dropdown.addItems(["Wood", "Steel", "Cement"])  # Add dummy items
        self.material_dropdown.setEditable(True)  # Make it searchable
        self.material_dropdown.lineEdit().setPlaceholderText("Search materials...")
        self.material_dropdown.setStyleSheet(f"""
            padding: 5px;
            border: 1px solid {color_palette['frame']};
            border-radius: 5px;
        """)
        input_layout.addWidget(self.material_dropdown)

        # Input field for mass
        self.mass_input = QLineEdit(input_frame)
        self.mass_input.setPlaceholderText("Enter mass")
        self.mass_input.setStyleSheet(f"""
            padding: 5px;
            border: 1px solid {color_palette['frame']};
            border-radius: 5px;
        """)
        input_layout.addWidget(self.mass_input)

        # Input field for emission factor
        self.emission_input = QLineEdit(input_frame)
        self.emission_input.setPlaceholderText("Enter carbon emission factor")
        self.emission_input.setStyleSheet(f"""
            padding: 5px;
            border: 1px solid {color_palette['frame']};
            border-radius: 5px;
        """)
        input_layout.addWidget(self.emission_input)

        # Predict button
        predict_button = QPushButton("Predict", input_frame)
        predict_button.clicked.connect(self.predict)
        predict_button.setStyleSheet(f"""
            background-color: {color_palette['button']};
            color: {color_palette['text']};
            border: 1px solid {color_palette['frame']};
            padding: 10px;
            border-radius: 5px;
            font-weight: bold;
        """)
        input_layout.addWidget(predict_button)

        # Add the input frame to the production layout
        production_layout.addWidget(input_frame)

        # Add the production layout to the central content layout
        self.central_content_layout.addLayout(production_layout)

    def load_model(self, model_path):
        # Reload model with the selected file
        self.model_handler = ModelHandler(model_path, self.total_features)
        QMessageBox.information(self, "Model Loaded", f"Model '{model_path}' has been loaded successfully.")

    def clear_central_content(self):
        # Remove all widgets from the central content layout
        while self.central_content_layout.count():
            item = self.central_content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def predict(self):
        material = self.material_dropdown.currentText()
        try:
            mass = float(self.mass_input.text())
            emission_factor = float(self.emission_input.text())
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter valid numeric values for mass and carbon emission factor.")
            return

        # Encoding map for categorical values (materials)
        encoding_map = {"Wood": 0, "Steel": 1, "Cement": 2}

        # Prepare feature vector
        feature_vector = prepare_features(material, [mass, emission_factor], encoding_map, self.total_features)
        
        # Ensure the feature vector has the correct shape
        feature_vector = np.array(feature_vector).reshape(1, -1)

        # Use the loaded model to predict
        try:
            prediction = self.model_handler.predict(material, [mass, emission_factor], encoding_map)
            # Display the result
            QMessageBox.information(self, "Prediction Result", f"The predicted output is: {prediction[0]}")
        except Exception as e:
            QMessageBox.critical(self, "Prediction Error", f"An error occurred during prediction: {str(e)}")

# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow('Gradient-Boosting-A1.pkl')  # Replace with your initial model path
    window.show()
    sys.exit(app.exec())
