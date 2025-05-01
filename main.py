import customtkinter as ctk
import sympy as sp
import matplotlib
import re
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Polygon
from sympy.parsing.latex import parse_latex
from sympy import symbols, sympify


matplotlib.use("TkAgg")


# custom components
class Entry(ctk.CTkFrame):
    def __init__(self, parent, labelText, placeholder=""):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="x", padx=20, pady=(10, 0))

        label = ctk.CTkLabel(
            self, text=labelText, anchor="w", justify="left", bg_color=self["bg"]
        )
        label.pack(anchor="w")
        self.main_entry = ctk.CTkEntry(
            self, placeholder_text=placeholder, bg_color=self["bg"]
        )

        self.main_entry.pack(fill="x")

    def return_entry(self):
        return self.main_entry

    def get_value(self):
        return self.main_entry.get()


class SelectOperation(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="x", padx=20, pady=10)
        self.sub_frame = None
        self.operation = None
        self.upper_entry = None
        self.lower_entry = None
        self.app = app
        
        options_frame = ctk.CTkFrame(self, fg_color="transparent")
        options_frame.pack(fill="x")

        self.options_var = ctk.StringVar(value="Choose")
        self.operation_combo = ctk.CTkComboBox(
            options_frame,
            values=["Derivative", "Integral"],
            command=self.options_save,
            variable=self.options_var,
        )
        self.operation_combo.pack(side="left", padx=4, pady=4, fill="x", expand=True)

        self.calculate_button = ctk.CTkButton(
            options_frame, text="Calculate", command=self.calculate
        )
        self.calculate_button.pack(side="right", padx=4, pady=4)

    def options_save(self, choice):
        if self.sub_frame:
            self.sub_frame.destroy()

        self.operation = choice

        if choice == "Derivative":
            self.derivative_options()
        elif choice == "Integral":
            self.integral_options()

    def integral_options(self):
        self.sub_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.sub_frame.pack(fill="x", pady=5)

        self.var_entry = Entry(
            self.sub_frame, "Variable of integration", "Default value is x"
        )
        self.upper_entry = Entry(
            self.sub_frame, "Upper bound (to)", "If bound is +inf, leave it blank"
        )
        self.lower_entry = Entry(
            self.sub_frame, "Lower bound (to)", "If bound is -inf, leave it blank"
        )

    def derivative_options(self):
        self.sub_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.sub_frame.pack(fill="x", pady=5)

        self.var_entry = Entry(
            self.sub_frame, "Differentiation variable", "Default value is x"
        )
        self.times_entry = Entry(
            self.sub_frame, "Differentiate how many times?", "Default value is 1"
        )

    def return_options(self):
        return self.var_entry, self.times_entry
    
    def return_integral_options(self):
        return self.upper_entry, self.lower_entry

    def calculate(self):
        try:
            function_text = self.app.function_entry.get_value()
            function_text = parse_latex(function_text)
            if not function_text:
                return

            var_name = self.var_entry.get_value() or "x"
            var = sp.symbols(var_name)
            expr = sp.sympify(function_text)
            print(expr)

            if self.operation == "Derivative":
                times = self.times_entry.get_value() or "1"
                result = sp.diff(expr, var, int(times))
                latex_result = sp.latex(result)

            elif self.operation == "Integral":
                lower = self.lower_entry.get_value()
                upper = self.upper_entry.get_value()
                if lower and upper:
                    lower = -sp.oo if lower == "-inf" else sp.sympify(lower)
                    upper = sp.oo if upper in ("inf", "+inf") else sp.sympify(upper)
                    result = sp.integrate(expr, (var, lower, upper))
                    latex_result = sp.latex(result)
                else:
                    result = sp.integrate(expr, var)
                    latex_result = sp.latex(result) + " + C"

            self.app.display_result(latex_result)
            self.app.result_plot_display.graph_equation()

        except Exception as e:
            print(f"Error: {str(e)}")


class ResultDisplay(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill="both", expand=True, padx=20, pady=10)

        fig = matplotlib.figure.Figure(figsize=(5, 1), dpi=100)
        self.wx = fig.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(fig, master=self)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # Configure the plot appearance
        fig.patch.set_facecolor("#2b2b2b")
        fig.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)

        # remove border
        self.wx.spines["top"].set_visible(False)
        self.wx.spines["right"].set_visible(False)
        self.wx.spines["bottom"].set_visible(False)
        self.wx.spines["left"].set_visible(False)
        self.wx.get_xaxis().set_visible(False)
        self.wx.get_yaxis().set_visible(False)
        self.wx.set_facecolor("#1f1f1f")

        plt.rcParams["text.color"] = "white"
        
    def display_result(self, result_text):
        formula = "$" + result_text + "$"
        self.wx.clear()
        self.wx.text(
            0.5, 0.5, formula, fontsize=15, ha="center", va="center", color="white"
        )
        self.canvas.draw()


class ShowEquation(ctk.CTkFrame):
    def __init__(self, parent, entry_widget):
        super().__init__(parent)
        self.pack(fill="both", expand=True, padx=10, pady=20)

        self.entry_widget = entry_widget
        self.entry_widget.main_entry.bind("<KeyRelease>", self.update_equation)

        fig = matplotlib.figure.Figure(figsize=(5, 1), dpi=100)
        self.wx = fig.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(fig, master=self)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        fig.patch.set_facecolor("#2b2b2b")
        fig.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)

        # remove border
        self.wx.spines["top"].set_visible(False)
        self.wx.spines["right"].set_visible(False)
        self.wx.spines["bottom"].set_visible(False)
        self.wx.spines["left"].set_visible(False)
        self.wx.get_xaxis().set_visible(False)
        self.wx.get_yaxis().set_visible(False)
        self.wx.set_facecolor("#1f1f1f")

        plt.rcParams["text.color"] = "white"

    def update_equation(self, text):
        text = self.entry_widget.get_value()
        if text:
            formula = "$" + text + "$"
        else:
            formula = "$f(x)$"

        self.wx.clear()
        self.wx.text(
            0.5, 0.5, formula, fontsize=20, ha="center", va="center", color="white"
        )
        self.canvas.draw()


class ShowGraph(ctk.CTkFrame):
    def __init__(self, parent, entry_widget, select_operation):
        super().__init__(parent)
        self.pack(fill="both", expand=True, padx=10, pady=20) 

        self.select_operation = select_operation
        self.entry_widget = entry_widget
        self.entry_widget.main_entry.bind("<KeyRelease>", self.graph_equation)

        fig = matplotlib.figure.Figure(figsize=(5, 4), dpi=100)
        self.wx = fig.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(fig, master=self)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        fig.patch.set_facecolor("#2b2b2b")
        fig.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)

        # Configure plot appearance
        self.wx.set_facecolor("#1f1f1f")
        self.wx.spines["top"].set_visible(False)
        self.wx.spines["right"].set_visible(False)
        self.wx.spines["bottom"].set_color("white")
        self.wx.spines["left"].set_color("white")
        self.wx.tick_params(axis="x", colors="white")
        self.wx.tick_params(axis="y", colors="white")
        plt.rcParams["text.color"] = "white"

    def graph_equation(self):
        print("Graph equation triggered")

        try:
            self.wx.clear()
            function_text = self.entry_widget.get_value()
            if not function_text:
                return

            function_text = parse_latex(function_text)
            expr = sp.sympify(function_text)
            var_name = self.select_operation.var_entry.get_value() or "x"
            var = sp.symbols(var_name)

            # Define x and y ranges
            x_vals = np.linspace(-10, 10, 500)
            y_vals = [float(expr.subs(var, x_val)) for x_val in x_vals]

            # Ensure the plot is reset
            self.wx.clear()
            self.wx.set_xlim(-10, 10)
            self.wx.set_ylim(min(y_vals) - 1, max(y_vals) + 1)

            # Plot the function
            self.wx.plot(x_vals, y_vals, label="f(x)", color="red", linewidth=2)

            # Optional: Fill the area for integrals
            if self.select_operation.operation == "Integral":
                lower = self.select_operation.lower_entry.get_value()
                upper = self.select_operation.upper_entry.get_value()
                if lower and upper:
                    lower = -sp.oo if lower == "-inf" else float(sp.sympify(lower))
                    upper = sp.oo if upper in ("inf", "+inf") else float(sp.sympify(upper))

                    x_fill = np.linspace(lower, upper, 500)
                    y_fill = [float(expr.subs(var, x_val)) for x_val in x_fill]
                    self.wx.fill_between(x_fill, y_fill, color="blue", alpha=0.3, label="Integral Area")

            # Re-draw the canvas and set axis labels
            self.wx.set_xlabel(var_name, color="white")
            self.wx.set_ylabel("f(x)", color="white")
            self.wx.legend(loc="upper left", fontsize=10, facecolor="#2b2b2b", edgecolor="white")

            self.canvas.draw()

        except Exception as e:
            print(f"Error in graphing: {e}")


    
# Main application class
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        window_width = 1200
        window_height = 700
        half_screen_width = int(self.winfo_screenwidth() / 2 - window_width / 2)
        half_screen_height = int(self.winfo_screenheight() / 2 - window_height / 2)

        self.title("Integral and Derivative Calculator")
        self.geometry(
            f"{window_width}x{window_height}+{half_screen_width}+{half_screen_height}"
        )
        self.minsize(1200, 600)

        # Create main frames
        self.left_frame = ctk.CTkFrame(self)
        self.left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self.right_frame = ctk.CTkFrame(self)
        self.right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Left frame content
        ctk.CTkLabel(
            self.left_frame,
            text="Integral and Derivative Calculator",
            font=("Arial", 24, "bold"),
        ).pack(pady=10)

        self.function_entry = Entry(
            self.left_frame,
            "Input Function",
            "Enter a mathematical expression like x^2 + 2*x",
        )

        ctk.CTkLabel(
            self.left_frame,
            text="Select Operation",
            font=("Arial", 20, "bold"),
        ).pack(pady=(30, 10))

        self.operation_selector = SelectOperation(self.left_frame, self)
        
        ctk.CTkLabel(
            self.left_frame,
            text="Equation Preview",
            font=("Arial", 20, "bold"),
        ).pack(pady=(20, 10))

        self.equation_display = ShowEquation(self.left_frame, self.function_entry)

        # Right frame content
        ctk.CTkLabel(
            self.right_frame,
            text="Result",
            font=("Arial", 20, "bold"),
        ).pack(pady=(20, 5))

        self.result_equation_display = ResultDisplay(self.right_frame)
        
        ctk.CTkLabel(
            self.right_frame,
            text="Graph",
            font=("Arial", 20, "bold"),
        ).pack(pady=(20, 5))
        
        self.result_plot_display = ShowGraph(self.right_frame, self.function_entry, self.operation_selector)

    def update_equation(self):
        self.equation_display.update_equation(None)

    def display_result(self, result):
        self.result_equation_display.display_result(result)
        self.result_plot_display.graph_equation()


if __name__ == "__main__":
    app = App()
    app.mainloop()
