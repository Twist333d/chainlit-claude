import base64
from PIL import Image
import io
import mimetypes
import os


def get_base64_encoded_image(image_path):
    try:
        # Check if the image exceeds the size limit
        if os.path.getsize(image_path) > 5 * 1024 * 1024:  # 5MB in bytes
            return "Error: Image exceeds the 5MB size limit."

        # Open the image and perform resizing and RGB conversion
        with Image.open(image_path) as img:
            max_size = (1024, 1024)
            img.thumbnail(max_size)  # Resize the image while maintaining its aspect ratio

            # Only convert to RGB if the image isn't PNG (preserve transparency for PNG)
            if img.format != 'PNG' and img.mode != 'RGB':
                img = img.convert('RGB')

            # Save the modified image to a temporary BytesIO stream
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format=img.format)  # Preserve the original format
            img_byte_arr.seek(0)

            # Read the binary data directly from the BytesIO stream
            binary_data = img_byte_arr.read()

        # Base64 encode the binary data
        base64_string = base64.b64encode(binary_data).decode('utf-8')
        return base64_string
    except Exception as e:
        return f"Error encoding image: {str(e)}"


def infer_mime_type(file_name):
    mime_type, _ = mimetypes.guess_type(file_name)
    return mime_type or 'application/octet-stream'