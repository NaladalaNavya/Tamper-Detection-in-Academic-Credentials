# Auto-orientation, resizing, cleanup
"""When you take a photo using a smartphone or digital camera, 
the sensor always saves the image in the same physical direction (typically "landscape"). 
If the phone was tilted (portrait, upside down, etc.), the device adds an EXIF tag called Orientation 
to tell software how to display the image properly.

This EXIF tag might say:

"This image is rotated 90° clockwise"

"This image is upside-down"

etc."""
from PIL import Image, ExifTags
import os

def auto_orient_image(input_path, output_path):
    try:
        img = Image.open(input_path)
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break

        exif = img._getexif()
        if exif is not None:
            orientation_value = exif.get(orientation, None)

            if orientation_value == 3:
                img = img.rotate(180, expand=True)
            elif orientation_value == 6:
                img = img.rotate(270, expand=True)
            elif orientation_value == 8:
                img = img.rotate(90, expand=True)

        img.save(output_path)
        print(f"✅ Oriented and saved: {output_path}")
    except Exception as e:
        print(f"⚠️ Error processing {input_path}: {e}")
