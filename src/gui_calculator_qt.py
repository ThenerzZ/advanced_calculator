from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QPushButton, QLineEdit, QVBoxLayout, QDialog
from PyQt6.QtCore import Qt
import sys
from operations.basic import add, subtract, multiply, divide 
from operations.advanced import power, square_root, logarithm, sin, cos, tan, pi, e, factorial
from operations.graphing import GraphingCanvas

class GraphDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Function Grapher")
        self.setMinimumSize(600, 400)
        
        self.setStyleSheet("""
            QDialog {
                background-color: #1C1C1E;
            }
            QLineEdit {
                padding: 10px;
                background-color: #2C2C2E;
                color: white;
                border: 1px solid #3C3C3E;
                border-radius: 8px;
                font-size: 16px;
                margin: 5px;
            }
            QPushButton {
                background-color: #FF9500;
                color: white;
                border: none;
                border-radius: 15px;
                padding: 10px;
                font-size: 16px;
                min-height: 35px;
                min-width: 80px;
                margin: 5px;
            }
            QPushButton:pressed {
                background-color: #CC7600;
            }
        """)
        
        layout = QVBoxLayout()
        
        self.function_input = QLineEdit()
        self.function_input.setPlaceholderText("Enter function (e.g., sin(x) or x**2)")
        layout.addWidget(self.function_input)
        
        self.canvas = GraphingCanvas(self)
        layout.addWidget(self.canvas)
        
        plot_button = QPushButton("Plot")
        plot_button.clicked.connect(self.plot)
        layout.addWidget(plot_button)
        
        self.setLayout(layout)
    
    def plot(self):
        expression = self.function_input.text()
        if not expression:
            return
        success = self.canvas.plot_function(expression)
        if not success:
            self.function_input.setText("Invalid expression - try again")
            self.function_input.selectAll()

class CalculatorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.memory = 0
        self.history = []
        self.current_theme = "dark"
        self.advanced_visible = False
        self.setWindowTitle("Calculator")
        self.setMinimumSize(350, 500)
        
        # Apply unified styling
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
                font-size: 40px;
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
                background-color: #E68500;
            }
            QPushButton#menu, QPushButton#graph {
                background-color: #323234;
                color: white;
                border-radius: 15px;
                font-size: 18px;
                min-height: 35px;
                min-width: 35px;
                margin: 5px;
            }
            QPushButton#menu:pressed, QPushButton#graph:pressed {
                background-color: #404042;
            }
        """)
        
        # Main layout setup
        self.generalLayout = QWidget()
        self.setCentralWidget(self.generalLayout)
        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(10, 10, 10, 10)
        self.generalLayout.setLayout(main_layout)
        
        # Top section with display and utility buttons
        top_widget = QWidget()
        top_layout = QGridLayout()
        top_layout.setContentsMargins(5, 5, 5, 5)
        top_widget.setLayout(top_layout)
        
        # Display setup
        self.display = QLineEdit()
        self.display.setFixedHeight(80)
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setReadOnly(True)
        top_layout.addWidget(self.display, 0, 0, 1, 4)
        
        # Utility buttons
        menu_btn = QPushButton('≡')
        menu_btn.setObjectName('menu')
        menu_btn.clicked.connect(self.toggle_advanced)
        top_layout.addWidget(menu_btn, 0, 4)
        
        graph_btn = QPushButton('📈')
        graph_btn.setObjectName('graph')
        graph_btn.clicked.connect(self.show_graph_dialog)
        top_layout.addWidget(graph_btn, 0, 5)
        
        main_layout.addWidget(top_widget)
        
        # Button grid
        button_widget = QWidget()
        self.layout = QGridLayout()
        self.layout.setSpacing(8)
        self.layout.setContentsMargins(15, 5, 15, 15)
        button_widget.setLayout(self.layout)
        main_layout.addWidget(button_widget)
        
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
        
        # Advanced buttons
        self.advanced_buttons = []
        advanced_button_texts = [
            ('sin', 1, 4), ('cos', 2, 4), ('tan', 3, 4),
            ('π', 4, 4), ('e', 5, 4),
            ('MC', 1, 5), ('MR', 2, 5), ('M+', 3, 5), ('M-', 4, 5)
        ]

        # Create basic buttons
        for button in basic_buttons:
            self.create_button(button)

        # Create advanced buttons (initially hidden)
        for button in advanced_button_texts:
            btn = self.create_button(button)
            btn.hide()
            self.advanced_buttons.append(btn)

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
        
        new_width = 500 if self.advanced_visible else 350
        self.setFixedWidth(new_width)

    def button_clicked(self, text):
        current = self.display.text()
        
        if text == 'C':
            self.display.clear()
        elif text == '=':
            try:
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
                result = {'sin': sin, 'cos': cos, 'tan': tan}[text](value)
                self.display.setText(str(result))
            except:
                self.display.setText('Error')
        elif text in ['MC', 'MR', 'M+', 'M-']:
            try:
                value = float(current)
                if text == 'MC':
                    self.memory = 0
                elif text == 'MR':
                    self.display.setText(str(self.memory))
                elif text == 'M+':
                    self.memory += value
                else:  # M-
                    self.memory -= value
            except:
                pass
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
        if Qt.Key.Key_0 <= key <= Qt.Key.Key_9:
            self.button_clicked(str(key - Qt.Key.Key_0))
        elif key in [Qt.Key.Key_Plus, Qt.Key.Key_Minus, Qt.Key.Key_Asterisk, Qt.Key.Key_Slash]:
            self.button_clicked({
                Qt.Key.Key_Plus: '+',
                Qt.Key.Key_Minus: '-',
                Qt.Key.Key_Asterisk: '×',
                Qt.Key.Key_Slash: '÷'
            }[key])

    def show_graph_dialog(self):
        """Show the graphing calculator dialog"""
        dialog = GraphDialog(self)
        dialog.exec()

def main():
    app = QApplication(sys.argv)
    window = CalculatorWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()