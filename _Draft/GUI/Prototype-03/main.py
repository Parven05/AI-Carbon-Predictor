from PySide6.QtWidgets import QApplication, QMainWindow, QMenuBar, QLabel, QVBoxLayout, QWidget, QTextEdit
from PySide6.QtGui import QAction, QPixmap
from PySide6.QtCore import Qt
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Carbon Predictor")
        self.setGeometry(100, 100, 910, 550)

        # Create the menu bar
        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)

        # Creating menu actions
        buttons = [
            "Get Started",
            "Production Stage",
            "Transportation to Factory Stage",
            "Manufacturing Stage",
            "Transportation to Site Stage",
            "Construction Stage",
            "Total Carbon Emission"
        ]

        for btn_text in buttons:
            action = QAction(btn_text, self)
            action.triggered.connect(lambda _, text=btn_text: self.on_button_clicked(text))
            menu_bar.addAction(action)

        # Create a central widget and layout for the main content area
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setAlignment(Qt.AlignCenter)  # Align the layout to center

        # Placeholder for image
        self.image_label = QLabel(self)
        self.layout.addWidget(self.image_label)

        # Text area below the image
        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)  # Make text read-only
        self.text_edit.setTextInteractionFlags(Qt.TextBrowserInteraction)  # Ensure text is viewable only
        self.text_edit.setText(
            """Welcome to the Carbon Emission Calculator!

Our tool is designed to help you estimate carbon emissions at construction sites across five key stages:

1. Production Stage (Emissions from raw material production)
2. Transportation of raw materials (Emissions from transporting raw materials to factories)
3. Manufacturing of raw materials (Emissions from the manufacturing process)
4. Transportation of materials to the construction site (Emissions from transporting materials to the site)
5. Construction activities on site (Emissions from on-site construction activities)

By providing accurate insights into your carbon footprint at each stage, we empower you to make informed decisions for a more sustainable construction process.
"""
        )
        self.text_edit.setStyleSheet("QTextEdit { border: none; }")  # Remove border

        # Add the text edit widget to the layout
        self.layout.addWidget(self.text_edit)

        # Set default view to "Get Started"
        self.on_button_clicked("Get Started")

    def on_button_clicked(self, button_name):
        if button_name == "Get Started":
            # Load and display the image
            pixmap = QPixmap("logo.png")  # Replace with your image path
            self.image_label.setPixmap(pixmap.scaled(
                300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation))  # Adjust size as needed
            self.image_label.setAlignment(Qt.AlignCenter)
            self.image_label.show()
            self.text_edit.show()
        else:
            self.image_label.hide()  # Hide the image if other menus are clicked
            self.text_edit.hide()    # Hide the text if other menus are clicked

        print(f"{button_name} menu item clicked")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
