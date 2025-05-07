from components.show_graph import ShowGraph
from components.show_equation import ShowEquation
from components.result_display import ResultDisplay
from components.calculator_entry import CalcEntry
from utils.select_operation import SelectOperation

import customtkinter as ctk
import tkinter as tk
import tkinter.messagebox

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

        self.function_entry = CalcEntry(
            self.left_frame,
        )
        self.function_entry.pack(padx=20, pady=(20, 0))
        self.equation_display = ShowEquation(self.left_frame, self.function_entry)
    
        self.operation_selector = SelectOperation(self.left_frame, self)

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
        self.result_plot_display.graph_equation()
        self.result_equation_display.display_result(result)

def on_closing():
    app.withdraw()
    app.quit()

if __name__ == "__main__":
    app = App()
    app.protocol("WM_DELETE_WINDOW", on_closing)
    app.mainloop()
