import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QMenuBar, QLabel, QVBoxLayout, 
                               QWidget, QTextEdit)
from PySide6.QtGui import QPixmap, QIcon, QAction
from PySide6.QtCore import Qt

from production import ProductionStageWindow
from transportation_to_factory import TransportationToFactoryStageWindow
from manufacturing import ManufacturingStageWindow
from transportation_to_site import TransportationToSiteStageWindow
from construction import ConstructionStageWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Smart Carbon Predictor")
        self.setWindowIcon(QIcon("resources/favicon.png"))
        self.setFixedSize(670, 560)

        self.setup_menu()
        self.setup_ui()

    def setup_menu(self):
        """Set up the menu bar and actions."""
        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)

        buttons = [
            "Production",
            "Transportation to Factory",
            "Manufacturing",
            "Transportation to Site",
            "Construction",
            "Total Carbon Emission"
        ]

        for btn_text in buttons:
            action = QAction(btn_text, self)
            action.triggered.connect(lambda _, text=btn_text: self.on_button_clicked(text))
            menu_bar.addAction(action)

    def setup_ui(self):
        """Set up the main UI components."""
        # Create a central widget and layout
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setAlignment(Qt.AlignCenter)

        # Placeholder for image
        self.image_label = QLabel(self)
        self.layout.addWidget(self.image_label)

        # Text area below the image
        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)
        self.text_edit.setTextInteractionFlags(Qt.TextBrowserInteraction)

        # Simplified stylesheet
        self.text_edit.setStyleSheet("""
            QTextEdit {
                background-color: #2C2C2C;
                color: white;
                border: none;
                padding: 10px;
            }
        """)
        
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
        self.layout.addWidget(self.text_edit)

        # Display logo and welcome text by default
        self.show_welcome_screen()

    def show_welcome_screen(self):
        """Display the welcome screen with the logo and introduction text."""
        pixmap = QPixmap("resources/logo.png")  # Replace with your image path
        self.image_label.setPixmap(pixmap.scaled(
            300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation))  # Adjust size as needed
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.show()
        self.text_edit.show()

    def on_button_clicked(self, button_name):
        """Handle button clicks and load respective windows."""
        if button_name == "Production":
            self.open_window(ProductionStageWindow())
        elif button_name == "Transportation to Factory": 
            self.open_window(TransportationToFactoryStageWindow())
        elif button_name == "Manufacturing":
            self.open_window(ManufacturingStageWindow())
        elif button_name == "Transportation to Site":
            self.open_window(TransportationToSiteStageWindow())
        elif button_name == "Construction":
            self.open_window(ConstructionStageWindow())
        elif button_name == "Total Carbon Emission":
            # Create and show window for Total Carbon Emission
            pass

    def open_window(self, window):
        """Open the given window as a dialog."""
        window.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    with open("styles.qss", "r") as file:
        app.setStyleSheet(file.read())

    window = MainWindow()
    window.show()
    sys.exit(app.exec())
