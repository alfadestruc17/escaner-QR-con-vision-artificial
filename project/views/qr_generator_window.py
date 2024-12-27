import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

class QRGeneratorWindow:
    def __init__(self, window, controller):
        self.window = window
        self.controller = controller
        self.window.title("Generate QR Code")
        self.setup_ui()

    def setup_ui(self):
        # Input frame
        input_frame = ttk.Frame(self.window)
        input_frame.pack(pady=10, padx=10)

        ttk.Label(input_frame, text="Enter data:").pack()
        self.data_entry = ttk.Entry(input_frame, width=40)
        self.data_entry.pack(pady=5)

        ttk.Label(input_frame, text="Created by:").pack()
        self.creator_entry = ttk.Entry(input_frame, width=40)
        self.creator_entry.pack(pady=5)

        ttk.Button(
            input_frame, 
            text="Generate", 
            command=self.generate_qr
        ).pack(pady=10)

        # Preview frame
        self.preview_frame = ttk.Frame(self.window)
        self.preview_frame.pack(pady=10, padx=10)

    def generate_qr(self):
        data = self.data_entry.get().strip()
        creator = self.creator_entry.get().strip()

        if not data:
            messagebox.showerror("Error", "Please enter data for the QR code")
            return

        try:
            filename = self.controller.generate_qr(data, creator)
            self.show_preview(filename)
            messagebox.showinfo("Success", "QR Code generated successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_preview(self, filename):
        image = Image.open(filename)
        image = image.resize((200, 200))
        photo = ImageTk.PhotoImage(image)

        if hasattr(self, 'preview_label'):
            self.preview_label.destroy()

        self.preview_label = ttk.Label(self.preview_frame, image=photo)
        self.preview_label.image = photo
        self.preview_label.pack()