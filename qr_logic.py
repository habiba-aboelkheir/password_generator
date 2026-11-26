from pathlib import Path
import qrcode


def create_qr_image(
    data: str,
    fill_color: str = "#38bdf8",
    back_color: str = "#0b1120",
    box_size: int = 10,
    border: int = 3,
):
    cleaned = data.strip()
    if not cleaned:
        raise ValueError("اكتب رابطًا أو نصًا أولًا لتوليد QR Code.")

    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=box_size,
        border=border,
    )
    qr.add_data(cleaned)
    qr.make(fit=True)

    return qr.make_image(fill_color=fill_color, back_color=back_color).convert("RGB")


def save_qr_image(img, file_path: str) -> Path:
    path = Path(file_path)
    if path.suffix.lower() != ".png":
        path = path.with_suffix(".png")
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path, format="PNG")
    return path