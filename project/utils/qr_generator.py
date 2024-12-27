import qrcode
from models.config import QR_VERSION, QR_ERROR_CORRECTION, QR_BOX_SIZE, QR_BORDER

def generate_qr_image(data: str, filename: str) -> None:
    qr = qrcode.QRCode(
        version=QR_VERSION,
        error_correction=getattr(qrcode.constants, f"ERROR_CORRECT_{QR_ERROR_CORRECTION}"),
        box_size=QR_BOX_SIZE,
        border=QR_BORDER,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    qr_image = qr.make_image(fill_color="black", back_color="white")
    qr_image.save(filename)