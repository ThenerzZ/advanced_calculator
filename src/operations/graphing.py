import numpy as np
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure

class GraphingCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        # Force matplotlib to use PyQt6 backend
        import matplotlib
        matplotlib.use('QtAgg')
        
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)
        self.axes.grid(True)
        
    def plot_function(self, expression, x_range=(-10, 10)):
        """Plot mathematical expression over given x range"""
        try:
            x = np.linspace(x_range[0], x_range[1], 1000)
            # Create safe namespace for evaluation
            namespace = {
                "x": x,
                "np": np,
                "sin": np.sin,
                "cos": np.cos,
                "tan": np.tan,
                "exp": np.exp,  # This is already here but making sure it's used
                "pi": np.pi,
                "e": np.e,
                # Add any other numpy functions you want to use
                "sqrt": np.sqrt,
                "log": np.log,
                "abs": np.abs
            }
            
            # Evaluate expression safely
            y = eval(expression, {"__builtins__": {}}, namespace)
            
            self.axes.clear()
            self.axes.plot(x, y)
            self.axes.grid(True)
            self.draw()
            return True
        except Exception as e:
            print(f"Plotting error: {str(e)}")
            return False

    def plot(self):
        expression = self.function_input.text()
        if not expression:
            return
            
        success = self.canvas.plot_function(expression)
        if not success:
            # Show error message in the input field
            self.function_input.setText("Invalid expression - try again")
            self.function_input.selectAll()