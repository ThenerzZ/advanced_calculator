from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QPushButton, QLineEdit
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
import sys
from operations.basic import add, subtract, multiply, divide
from operations.advanced import power, square_root, logarithm

class CalculatorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculator")
        self.setMinimumSize(350, 500)  # Smaller minimum size
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1C1C1E;
            }
            QLineEdit {
                padding: 15px;
                background-color: #1C1C1E;
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 36px;
                margin: 5px;
            }
            QPushButton {
                background-color: #2C2C2E;
                color: white;
                border: none;
                border-radius: 25px;
                padding: 15px;
                font-size: 20px;
                min-height: 50px;
                min-width: 50px;
                margin: 3px;
            }
            QPushButton:pressed {
                background-color: #3C3C3E;
            }
            QPushButton#operator {
                background-color: #FF9500;
                color: white;
            }
            QPushButton#operator:pressed {
                background-color: #FF9F0A;
            }
        """)

        self.generalLayout = QWidget()
        self.setCentralWidget(self.generalLayout)
        self.layout = QGridLayout()
        self.layout.setSpacing(10)  # Add spacing between widgets
        self.layout.setContentsMargins(20, 20, 20, 20)  # Add margins around the layout
        self.generalLayout.setLayout(self.layout)
        
        # Make display taller
        self.display = QLineEdit()
        self.display.setFixedHeight(100)  # Increase display height
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setReadOnly(True)
        
        # Make display span all columns and add more vertical space
        self.layout.addWidget(self.display, 0, 0, 1, 4)
        self.layout.setRowStretch(0, 2)  # Give more vertical space to display
        
        self.create_buttons()

    def create_buttons(self):
        button_texts = [
            ('C', 1, 0), ('±', 1, 1), ('%', 1, 2), ('÷', 1, 3),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('×', 2, 3),
            ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('-', 3, 3),
            ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('+', 4, 3),
            ('0', 5, 0, 1, 2), ('.', 5, 2), ('=', 5, 3)
        ]
        
        for button in button_texts:
            text = button[0]
            row = button[1]
            col = button[2]
            
            btn = QPushButton(text)
            if len(button) > 3:  # For the zero button that spans multiple columns
                self.layout.addWidget(btn, row, col, 1, button[3])
            else:
                self.layout.addWidget(btn, row, col)
                
            if text in '÷×-+=':
                btn.setProperty('class', 'operator')
                btn.setObjectName('operator')
                
            btn.clicked.connect(lambda checked, text=text: self.button_clicked(text))
        
        # Add stretch to make layout expand properly
        self.layout.setRowStretch(6, 1)
        for i in range(4):
            self.layout.setColumnStretch(i, 1)
            
    def button_clicked(self, text):
        current = self.display.text()
        
        if text == 'C':
            self.display.clear()
        elif text == '=':
            try:
                # Replace symbols with operators
                expression = current.replace('×', '*').replace('÷', '/')
                result = eval(expression)
                self.display.setText(str(result))
            except Exception:
                self.display.setText('Error')
        elif text == '±':
            try:
                value = float(current)
                self.display.setText(str(-value))
            except:
                pass
        elif text == '%':
            try:
                value = float(current)
                self.display.setText(str(value/100))
            except:
                pass
        else:
            self.display.setText(current + text)

def main():
    app = QApplication(sys.argv)
    window = CalculatorWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()