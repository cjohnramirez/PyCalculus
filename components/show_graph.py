import customtkinter as ctk
import sympy as sp
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sympy.parsing.latex import parse_latex

matplotlib.use("TkAgg")


class ShowGraph(ctk.CTkFrame):
    def __init__(self, parent, entry_widget, select_operation):
        super().__init__(parent)
        self.pack(fill="both", expand=True, padx=10, pady=20)

        self.select_operation = select_operation
        self.entry_widget = entry_widget

        fig = matplotlib.figure.Figure(figsize=(5, 4), dpi=100)
        self.wx = fig.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(fig, master=self)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        fig.patch.set_facecolor("#2b2b2b")
        fig, ax = plt.subplots(figsize=(6, 4))
        fig.tight_layout()

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

            self.wx.set_ylim(min(y_vals) - 10, max(y_vals) + 10)
            self.wx.axhline(
                0, color="white", linewidth=0.8
            )  # Add horizontal line at y=0
            self.wx.axvline(0, color="white", linewidth=0.8)  # Add vertical line at x=0

            # Plot the function
            self.wx.plot(x_vals, y_vals, label="f(x)", color="red", linewidth=2)

            if self.select_operation.operation == "Derivative":
                times = self.select_operation.times_entry.get_value() or "1"
                derivative = sp.diff(expr, var, int(times))
                derivative_vals = [
                    float(derivative.subs(var, x_val)) for x_val in x_vals
                ]
                self.wx.plot(
                    x_vals,
                    derivative_vals,
                    label=f"f{'`' * int(times)}(x)",
                    color="blue",
                    linewidth=2,
                )

            # Optional: Fill the area for integrals
            if self.select_operation.operation == "Integral":
                lower = self.select_operation.lower_entry.get_value()
                upper = self.select_operation.upper_entry.get_value()
                if lower and upper:
                    lower = -sp.oo if lower == "-inf" else float(sp.sympify(lower))
                    upper = (
                        sp.oo if upper in ("inf", "+inf") else float(sp.sympify(upper))
                    )

                    x = np.linspace(lower, upper, 500)
                    y = np.array([float(expr.subs(var, val)) for val in x])

                    x_margin = 0.05 * (upper - lower)
                    x_fill = x[(x > lower + x_margin) & (x < upper - x_margin)]
                    y_fill = np.array([float(expr.subs(var, val)) for val in x_fill])

                    self.wx.cla()
                    self.wx.plot(x, y, color='red', linewidth=2, label="f(x)")
                    self.wx.fill_between(x_fill, y_fill, color='blue', alpha=0.5, label="Integral Area")
                    
                    self.wx.set_xlim(lower, upper)
                    self.wx.set_ylim(np.min(y), np.max(y))
                    self.wx.axhline(0, color='white', linewidth=1)
                    self.wx.axvline(0, color='white', linewidth=1)
                    self.wx.margins(0)


            # Re-draw the canvas and set axis labels
            self.wx.set_xlabel(var_name, color="white")
            self.wx.set_ylabel("f(x)", color="white")
            self.wx.legend(
                loc="upper left", fontsize=10, facecolor="#2b2b2b", edgecolor="white"
            )

            self.canvas.draw()

        except Exception as e:
            print(f"Error in graphing: {e}")
