import customtkinter as ctk

class CalcEntry(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="x")

        self.main_entry = ctk.CTkEntry(
            self, bg_color=self["bg"], height=40, font=("Roboto", 12), text_color="white", placeholder_text="Enter your equation here"
        )

        self.main_entry.pack(fill="x")

    def return_entry(self):
        return self.main_entry

    def get_value(self):
        return self.main_entry.get()