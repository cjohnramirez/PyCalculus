from components.custom_entry import Entry

import customtkinter as ctk
import sympy as sp
from sympy.parsing.latex import parse_latex
from sympy import N

class SelectOperation(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="x", padx=20)
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
        self.operation_combo.pack(side="left", fill="x", expand=True, pady=(0, 20))

        self.calculate_button = ctk.CTkButton(
            options_frame, text="Calculate", command=self.calculate
        )
        self.calculate_button.pack(side="right", padx=(10, 0), pady=(0, 20))

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
        self.sub_frame.pack(fill="both")

        self.var_entry = Entry(
            self.sub_frame, "Variable of integration", "Default value is x"
        )
        self.var_entry.pack(fill="both", side="left", padx=(0, 10), expand=True)
        self.upper_entry = Entry(
            self.sub_frame, "Upper bound (to)", "Default is +inf"
        )
        self.upper_entry.pack(fill="x", side="left", padx=(0, 10), expand=True)
        self.lower_entry = Entry(
            self.sub_frame, "Lower bound (to)", "Default is -inf"
        )
        self.lower_entry.pack(fill="both", side="left", expand=True)

    def derivative_options(self):
        self.sub_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.sub_frame.pack(fill="both")

        self.var_entry = Entry(
            self.sub_frame, "Differentiation variable", "Default value is x"
        )
        self.var_entry.pack(fill="x", side="left", padx=(0, 10))
        self.times_entry = Entry(
            self.sub_frame, "Differentiate how many times?", "Default value is 1"
        )
        self.times_entry.pack(fill="x", side="left")

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
                    result = N(result)
                    latex_result = sp.latex(result)
                else:
                    result = sp.integrate(expr, var)
                    latex_result = sp.latex(result) + " + C"

            self.app.display_result(latex_result)
            self.app.result_plot_display.graph_equation()

        except Exception as e:
            print(f"Error: {str(e)}")