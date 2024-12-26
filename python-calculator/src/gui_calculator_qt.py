from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QPushButton, QLineEdit, QVBoxLayout, QDialog
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
import sys
from operations.basic import add, subtract, multiply, divide
from operations.advanced import power, square_root, logarithm
from operations.graphing import GraphingCanvas
from math import sin, cos, tan, pi, e, factorial

class GraphDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Function Grapher")
        self.setMinimumSize(600, 400)
        
        layout = QVBoxLayout()
        
        # Function input
        self.function_input = QLineEdit()
        self.function_input.setPlaceholderText("Enter function (e.g., sin(x) or x**2)")
        layout.addWidget(self.function_input)
        
        # Graph canvas
        self.canvas = GraphingCanvas(self)
        layout.addWidget(self.canvas)
        
        # Plot button
        plot_button = QPushButton("Plot")
        plot_button.clicked.connect(self.plot)
        layout.addWidget(plot_button)
        
        self.setLayout(layout)
    
    def plot(self):
        expression = self.function_input.text()
        self.canvas.plot_function(expression)

class CalculatorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.memory = 0
        self.history = []
        self.current_theme = "dark"
        self.advanced_visible = False
        self.setWindowTitle("Calculator")
        self.setMinimumSize(350, 500)  # Smaller minimum size
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1C1C1E;
            }
            QLineEdit {
                padding: 15px;
                background-color: #2C2C2E;
                color: white;
                border: 2px solid #3C3C3E;
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
            QPushButton#advanced {
                background-color: #147EFB;
                color: white;
            }
            QPushButton#advanced:pressed {
                background-color: #0A5CD6;
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
        # Basic buttons
        basic_buttons = [
            ('C', 1, 0), ('±', 1, 1), ('%', 1, 2), ('÷', 1, 3),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('×', 2, 3),
            ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('-', 3, 3),
            ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('+', 4, 3),
            ('0', 5, 0, 1, 2), ('.', 5, 2), ('=', 5, 3)
        ]
        
        # Advanced buttons (initially hidden)
        self.advanced_buttons = []
        advanced_button_texts = [
            ('sin', 1, 4), ('cos', 2, 4), ('tan', 3, 4),
            ('π', 4, 4), ('e', 5, 4), ('x!', 6, 4),
            ('MC', 1, 5), ('MR', 2, 5), ('M+', 3, 5), ('M-', 4, 5)
        ]

        # Create basic buttons
        for button in basic_buttons:
            self.create_button(button)

        # Create advanced buttons (hidden initially)
        for button in advanced_button_texts:
            btn = self.create_button(button)
            btn.hide()
            self.advanced_buttons.append(btn)

        # Add advanced toggle button
        toggle_btn = QPushButton('≡')
        toggle_btn.setObjectName('advanced')
        toggle_btn.clicked.connect(self.toggle_advanced)
        self.layout.addWidget(toggle_btn, 6, 3)
        
        # Add graph button
        graph_btn = QPushButton('📈')
        graph_btn.setObjectName('advanced')
        graph_btn.clicked.connect(self.show_graph_dialog)
        self.layout.addWidget(graph_btn, 6, 4)

    def create_button(self, button_info):
        text = button_info[0]
        row = button_info[1]
        col = button_info[2]
        
        btn = QPushButton(text)
        if len(button_info) > 3:
            self.layout.addWidget(btn, row, col, 1, button_info[3])
        else:
            self.layout.addWidget(btn, row, col)
            
        if text in '÷×-+=':
            btn.setObjectName('operator')
            
        btn.clicked.connect(lambda checked, text=text: self.button_clicked(text))
        return btn

    def toggle_advanced(self):
        self.advanced_visible = not self.advanced_visible
        for btn in self.advanced_buttons:
            btn.setVisible(self.advanced_visible)
        
        # Adjust window size
        if self.advanced_visible:
            self.setMinimumWidth(500)
        else:
            self.setMinimumWidth(350)
            
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
                self.add_to_history(expression, result)
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
        elif text in ['sin', 'cos', 'tan']:
            try:
                value = float(current)
                if text == 'sin':
                    result = sin(value)
                elif text == 'cos':
                    result = cos(value)
                else:
                    result = tan(value)
                self.display.setText(str(result))
            except:
                self.display.setText('Error')
        elif text == 'x!':
            try:
                value = int(float(current))
                result = factorial(value)
                self.display.setText(str(result))
            except:
                self.display.setText('Error')
        elif text == 'π':
            self.display.setText(str(pi))
        elif text == 'e':
            self.display.setText(str(e))
        else:
            self.display.setText(current + text)

    def add_to_history(self, expression, result):
        self.history.append(f"{expression} = {result}")

    def keyPressEvent(self, event):
        key = event.key()
        # Use correct Qt.Key enum values for PyQt6
        if Qt.Key.Key_0 <= key <= Qt.Key.Key_9:
            self.button_clicked(str(key - Qt.Key.Key_0))
        elif key in [Qt.Key.Key_Plus, Qt.Key.Key_Minus, Qt.Key.Key_Asterisk, Qt.Key.Key_Slash]:
            self.button_clicked({
                Qt.Key.Key_Plus: '+',
                Qt.Key.Key_Minus: '-',
                Qt.Key.Key_Asterisk: '×',
                Qt.Key.Key_Slash: '÷'
            }[key])

    def toggle_theme(self):
        if self.current_theme == "dark":
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #f0f0f0;
                }
                QLineEdit {
                    background-color: #ffffff;
                    color: #000000;
                    /* ... other styles ... */
                }
                /* ... other light theme styles ... */
            """)
            self.current_theme = "light"
        else:
            # Revert to original dark theme
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
            self.current_theme = "dark"
            
    def show_graph_dialog(self):
        dialog = GraphDialog(self)
        dialog.exec()

def main():
    app = QApplication(sys.argv)
    window = CalculatorWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()