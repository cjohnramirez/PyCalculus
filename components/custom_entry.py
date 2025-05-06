import customtkinter as ctk

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