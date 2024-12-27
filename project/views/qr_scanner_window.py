import tkinter as tk
from tkinter import ttk, messagebox
import cv2
from PIL import Image, ImageTk

class QRScannerWindow:
    def __init__(self, window, controller):
        self.window = window
        self.controller = controller
        self.window.title("Scan QR Code")
        self.setup_ui()
        self.start_camera()

    def setup_ui(self):
        # Camera frame
        self.camera_frame = ttk.Label(self.window)
        self.camera_frame.pack(pady=10)

        # Info frame
        self.info_frame = ttk.Frame(self.window)
        self.info_frame.pack(pady=10, padx=10)
        
        self.info_label = ttk.Label(self.info_frame, text="Scanning...")
        self.info_label.pack()

        # Entry status
        self.entry_label = ttk.Label(self.info_frame, text="")
        self.entry_label.pack(pady=5)

    def start_camera(self):
        if self.controller.start_camera():
            self.update_camera()
        else:
            messagebox.showerror("Error", "Failed to start camera")
            self.window.destroy()

    def update_camera(self):
        if not self.window.winfo_exists():
            self.controller.stop_camera()
            return

        frame, qr_data = self.controller.process_camera_frame()
        
        if frame is not None:
            # Update camera feed
            image = Image.fromarray(frame)
            image = image.resize((640, 480))
            photo = ImageTk.PhotoImage(image=image)
            self.camera_frame.configure(image=photo)
            self.camera_frame.image = photo

            # Update QR info if detected
            if qr_data:
                self.info_label.config(text=f"Detected: {qr_data}")
                success, message = self.controller.process_qr_scan(qr_data)
                self.entry_label.config(
                    text=message,
                    foreground="green" if success else "red"
                )

        self.window.after(10, self.update_camera)