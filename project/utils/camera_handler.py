import cv2
from pyzbar import pyzbar

def process_frame(frame):
    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detect QR codes
    qr_codes = pyzbar.decode(gray)
    qr_data = None
    
    for qr in qr_codes:
        # Extract data
        qr_data = qr.data.decode('utf-8')
        
        # Draw rectangle around QR code
        (x, y, w, h) = qr.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # Add text with QR data
        cv2.putText(
            frame, qr_data, (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2
        )
        break  # Process only the first QR code found

    # Convert to RGB for tkinter
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return frame_rgb, qr_data