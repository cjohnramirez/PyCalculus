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

    def add_entry(self, value):
        self.main_entry.insert("end", value)
        
    def clear_entry(self):
        self.main_entry.delete(0, "end")
        
    def backspace_entry(self):
        current_text = self.main_entry.get()
        if current_text:
            self.main_entry.delete(len(current_text) - 1, "end")