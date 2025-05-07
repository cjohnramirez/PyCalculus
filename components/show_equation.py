import customtkinter as ctk
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

matplotlib.use("TkAgg")


class ShowEquation(ctk.CTkFrame):
    def __init__(self, parent, entry_widget):
        super().__init__(parent, border_color="white", border_width=2)
        self.pack(fill="x", pady=20, padx=20)
        self.entry_widget = entry_widget
        self.entry_widget.main_entry.bind("<KeyRelease>", self.update_equation)

        fig = matplotlib.figure.Figure(figsize=(5, 1), dpi=100)
        self.wx = fig.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(fig, master=self)
        self.canvas.get_tk_widget().pack(fill="x")

        fig.patch.set_facecolor("#2b2b2b")

        # remove border
        self.wx.spines["top"].set_visible(False)
        self.wx.spines["right"].set_visible(False)
        self.wx.spines["bottom"].set_visible(False)
        self.wx.spines["left"].set_visible(False)
        self.wx.get_xaxis().set_visible(False)
        self.wx.get_yaxis().set_visible(False)
        self.wx.set_facecolor("#2b2b2b")

        plt.rcParams["text.color"] = "white"

    def update_equation(self, text):    
        text = self.entry_widget.get_value()

        if text:
            formula = "$" + text + "$"
        else:
            formula = "$Equation \ shows \ here$"

        self.wx.clear()
        self.wx.text(
            0.5, 0.5, formula, fontsize=20, ha="center", va="center", color="white"
        )
        self.canvas.draw()
