import cv2
import logging
from datetime import datetime
import os
from utils.qr_generator import generate_qr_image
from utils.camera_handler import process_frame

class QRController:
    def __init__(self, qr_model):
        self.model = qr_model
        self.cap = None

    def generate_qr(self, data: str, created_by: str) -> str:
        try:
            # Generate and save QR image
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"qr_codes/qr_{timestamp}.png"
            generate_qr_image(data, filename)

            # Store in database
            self.model.create_qr(data, created_by)
            
            logging.info(f"QR Code generated: {filename}")
            return filename
        except Exception as e:
            logging.error(f"Error in generate_qr: {e}")
            raise

    def start_camera(self) -> bool:
        try:
            self.cap = cv2.VideoCapture(0)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            return True
        except Exception as e:
            logging.error(f"Error starting camera: {e}")
            return False

    def process_camera_frame(self):
        if self.cap is None:
            return None, None

        ret, frame = self.cap.read()
        if not ret:
            return None, None

        return process_frame(frame)

    def process_qr_scan(self, qr_data: str) -> tuple:
        try:
            qr_info = self.model.get_qr_by_data(qr_data)
            if not qr_info:
                return False, "QR code not found in database"

            # Record scan with full data
            self.model.record_scan(qr_info['id'], "Main Scanner", qr_info)
            
            # Record entry with full data
            return self.model.record_entry(qr_info['id'], qr_info)
        except Exception as e:
            logging.error(f"Error processing scan: {e}")
            return False, str(e)

    def stop_camera(self):
        if self.cap:
            self.cap.release()
            cv2.destroyAllWindows()