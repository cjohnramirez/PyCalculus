from components.show_graph import ShowGraph
from components.show_equation import ShowEquation
from components.result_display import ResultDisplay
from components.custom_entry import Entry
from utils.select_operation import SelectOperation

import customtkinter as ctk
import matplotlib

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
