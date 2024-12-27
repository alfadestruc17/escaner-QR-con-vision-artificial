import tkinter as tk
import logging
import os
from models.database import Database
from models.qr_code import QRCodeModel
from controllers.qr_controller import QRController
from views.main_window import MainWindow

def main():
    # Create QR codes directory
    os.makedirs("qr_codes", exist_ok=True)

    # Set up logging
    logging.basicConfig(
        filename='qr_system.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    try:
        # Initialize database and models
        db = Database()
        qr_model = QRCodeModel(db)
        
        # Initialize controller
        controller = QRController(qr_model)

        # Start GUI
        root = tk.Tk()
        app = MainWindow(root, controller)
        root.mainloop()

    except Exception as e:
        logging.error(f"Application error: {e}")
        raise
    finally:
        if 'db' in locals():
            db.close()

if __name__ == "__main__":
    main()