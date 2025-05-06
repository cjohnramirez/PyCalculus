import customtkinter as ctk
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


matplotlib.use("TkAgg")


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
