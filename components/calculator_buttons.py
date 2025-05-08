import customtkinter as ctk


class CalcButtons(ctk.CTkFrame):
    def __init__(self, parent, calculator_entry):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="x")
        self.update_entry = calculator_entry

        self.inverse_mode = False
        self.button_widgets = []

        self.calculator_buttons = [
            [
                ["Inv", "Inv"],
                ["sin", r"\sin("],
                ["x!", "!"],
                ["(", "("],
                [")", ")"],
                ["CE", "CE"],
                ["Clear", "Clear"],
            ],
            [
                ["π", r"\pi"],
                ["cos", r"\cos("],
                ["ln", r"\ln("],
                ["7", "7"],
                ["8", "8"],
                ["9", "9"],
                ["÷", "/"],
            ],
            [
                ["e", r"\exp("],
                ["tan", r"\tan("],
                ["log", r"\log("],
                ["4", "4"],
                ["5", "5"],
                ["6", "6"],
                ["x", "x"],
            ],
            [
                ["√", r"\sqrt("],
                ["|x|", r"\abs("],
                ["x", "x"],
                ["1", "1"],
                ["2", "2"],
                ["3", "3"],
                ["-", "-"],
            ],
            [
                ["Ans", "Ans"],
                ["x²", "^2"],
                ["xʸ", "^"],
                ["0", "0"],
                [".", "."],
                ["=", "="],
                ["+", "+"],
            ],
        ]

        self.build_buttons()

    def build_buttons(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.button_widgets.clear()

        for row_index, row in enumerate(self.calculator_buttons):
            row_frame = ctk.CTkFrame(self, fg_color="transparent")
            row_frame.pack(fill="x", pady=(0, 10), expand=True)

            for col_index, button in enumerate(row):
                label, equation = button
                if label == "Clear":
                    btn = ctk.CTkButton(
                        row_frame,
                        text=label,
                        command=self.clear_entry,
                        width=75,
                        height=40,
                        font=("Roboto", 12),
                    )
                elif label == "CE":
                    btn = ctk.CTkButton(
                        row_frame,
                        text=label,
                        command=self.backspace_entry,
                        width=75,
                        height=40,
                        font=("Roboto", 12),
                    )
                elif label.startswith("Inv"):
                    btn = ctk.CTkButton(
                        row_frame,
                        text=label,
                        command=self.inverse_functions,
                        width=75,
                        height=40,
                        font=("Roboto", 12),
                    )
                    self.inv_button = btn
                else:
                    btn = ctk.CTkButton(
                        row_frame,
                        text=label,
                        command=lambda eq=equation: self.add_to_entry(eq),
                        width=75,
                        height=40,
                        font=("Roboto", 12),
                    )
                btn.pack(side="left", padx=(0, 10), pady=(20, 0), expand=True)
                self.button_widgets.append(btn)

    def add_to_entry(self, equation):
        self.update_entry.add_entry(equation)

    def clear_entry(self):
        self.update_entry.clear_entry()

    def backspace_entry(self):
        self.update_entry.backspace_entry()

    def inverse_functions(self):
        self.inverse_mode = not self.inverse_mode

        if self.inverse_mode:
            self.calculator_buttons[0][0] = ["Inv⁻¹", "Inv⁻¹"]
            self.calculator_buttons[0][1] = ["sin⁻¹", r"\arcsin("]
            self.calculator_buttons[1][1] = ["cos⁻¹", r"\arccos("]
            self.calculator_buttons[2][1] = ["tan⁻¹", r"\arctan("]
        else:
            self.calculator_buttons[0][0] = ["Inv", "Inv"]
            self.calculator_buttons[0][1] = ["sin", r"\sin("]
            self.calculator_buttons[1][1] = ["cos", r"\cos("]
            self.calculator_buttons[2][1] = ["tan", r"\tan("]

        self.build_buttons()
