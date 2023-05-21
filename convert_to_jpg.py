from tkinter import messagebox
from PIL import Image, ImageTk
import os

class ImageConverter:
    def __init__(self):
        self.image_paths = []
    def convert_to_jpg(self, image_path, output_folder):
        try:
            im = Image.open(image_path)
            im = im.convert("RGB")

            # Get the original filename without extension
            filename = os.path.splitext(os.path.basename(image_path))[0]

            # Make the output path inside the output folder
            output_path = os.path.join(output_folder, f"{filename}.jpg")  # Fix: Save as JPEG format
            im.save(output_path, "JPEG")  # Fix: Save to the correct output path
            return True
        except OSError as e:
            messagebox.showerror("Failed to convert image", f"Error: {e}")
            return False
    def convert(self):
        output_folder = None
        converted_count = 0
        for image_path in self.image_paths:
            if image_path:
                if output_folder is None:
                    output_folder = os.path.join(os.path.dirname(image_path), "output")
                    try:
                        os.makedirs(output_folder, exist_ok=True)
                    except OSError as e:
                        messagebox.showerror("Folder Creation Error", f"Failed to create folder: {output_folder}\nError: {e}")
                        return
                if self.convert_to_jpg(image_path=image_path, output_folder=output_folder):
                    converted_count += 1
        if converted_count == len(self.image_paths):
            messagebox.showinfo("Conversion Completed", f"All {converted_count} images were converted successfully")
        else:
            messagebox.showinfo("Conversion Complete", "Some images failed to convert")