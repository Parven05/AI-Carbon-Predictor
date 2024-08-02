MAIN_WINDOW_STYLE = """
QWidget {
    font-family: 'Roboto', sans-serif;
    background-color: #F5F5F5;

}

QListWidget {
    background-color: #333;
    color: #FFF;
    border: 1px solid #888;
    padding-top: 20px;
}

QListWidget::item {
    padding: 8px;
    margin: 2px;
    border-radius: 3px;
    font-size: 12px;
    font-weight: normal;
    text-align: center;
}

QListWidget::item:selected {
    background-color: #555;
    border: 1px solid #999;
}

QComboBox, QLineEdit {
    background-color: #EEE;
    border: 1px solid #CCC;
    padding: 5px;
    border-radius: 3px;
}

QPushButton {
    background-color: #666;
    color: #FFF;
    border: 1px solid #888;
    padding: 8px;
    font-size: 14px;
    border-radius: 3px;
}

QPushButton:hover {
    background-color: #888;
}

QLabel {
    font-size: 14px;
    color: #333;
}
"""
