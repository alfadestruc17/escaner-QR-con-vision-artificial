import tkinter as tk
from tkinter import ttk
from .qr_generator_window import QRGeneratorWindow
from .qr_scanner_window import QRScannerWindow

class MainWindow:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.root.title("QR Code System")
        self.setup_ui()

    def setup_ui(self):
        # Main buttons
        ttk.Button(
            self.root, 
            text="Generate QR", 
            command=self.show_generator
        ).pack(pady=10)
        
        ttk.Button(
            self.root, 
            text="Scan QR", 
            command=self.show_scanner
        ).pack(pady=10)

    def show_generator(self):
        QRGeneratorWindow(tk.Toplevel(self.root), self.controller)

    def show_scanner(self):
        QRScannerWindow(tk.Toplevel(self.root), self.controller)