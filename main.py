from tkinter import *
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import messagebox
from convert_to_jpg import ImageConverter
from convert_to_png import PngConverter
from brightness import Brightness
from PIL import Image, ImageTk, ImageEnhance

root = Tk()
root.title("image convertor")
root.geometry("500x500")

image_paths = []
original_image = None
edited_image = None
image_item = None

def open():
    global image_paths, image_item, edited_image, original_image
    image_paths = filedialog.askopenfilenames()
    image_converter.image_paths = image_paths
    png_image_converter.image_paths = image_paths 
    if len(image_paths) > 0:
        image_path = image_paths[0]
        original_image = Image.open(image_path)
        edited_image = original_image.copy()
        width = original_image.width // 2
        height = original_image.height // 2
        original_image = original_image.resize((width, height))
        edited_image = edited_image.resize((width, height))
        image_tk = ImageTk.PhotoImage(original_image)
        if image_item:
            canvas.delete(image_item)
        image_item = canvas.create_image(0, 0, anchor=NW, image=image_tk)
        canvas.image = image_tk

def convert_images():
    image_converter.convert()

def png_convert():
    png_image_converter.convert()

    
def rotate_image():
    global image_item, edited_image, original_image
    try:
        if edited_image is not None:
            edited_image = edited_image.rotate(angle=90, expand=True)
            rotated_image = edited_image
        else:
            original_image = original_image.rotate(angle=90, expand=True)
            rotated_image = original_image

        image_tk = ImageTk.PhotoImage(rotated_image)
        canvas.itemconfig(image_item, image=image_tk)
        canvas.image = image_tk
        canvas.config(width=rotated_image.width, height=rotated_image.height)  # Update canvas dimensions

    except OSError as e:
        messagebox.showerror("Failed to rotate image", f"Error: {e}")
        return False
        


def brightness():
    global image_paths, image_item, original_image, edited_image
    try:
        bright_image = edited_image if edited_image is not None else original_image
        bright_image = bright_image.convert("RGB")
        BrightValue = simpledialog.askfloat("Input", "Enter the value :")
        enhancer = ImageEnhance.Brightness(bright_image)
        adjusted_image = enhancer.enhance(BrightValue)
        img_tk = ImageTk.PhotoImage(adjusted_image)
        canvas.itemconfig(image_item, image=img_tk)
        canvas.image = img_tk
        return True

    except OSError as e:
        messagebox.showerror("Failed to enhance brightness", f"Error: {e}")
        return False

def save_file():
    global edited_image
    if edited_image:
        if save_path := filedialog.asksaveasfilename(
            defaultextension=".jpg",
            filetypes=[("JPEG Image", "*.jpg"), ("PNG Image", "*.png")],
        ):
            edited_image.save(save_path)

image_converter = ImageConverter()
png_image_converter = PngConverter()


menu_bar = Menu(root)
root.config(menu=menu_bar)

file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Open", command=open)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

edit_menu = Menu(menu_bar, tearoff=0)

batch_convert = Menu(edit_menu)
edit_menu.add_cascade(label="Batch convert",menu=batch_convert)
batch_convert.add_command(label="Convert to JPEG", command=convert_images)
batch_convert.add_command(label="Convert to png", command=png_convert)

edit_menu.add_command(label="Brightness", command=brightness)

rotate_menu = Menu(edit_menu)
edit_menu.add_cascade(label="Rotate", menu=rotate_menu)
rotate_menu.add_command(label="⬅️ Rotate 90", command=rotate_image)


menu_bar.add_cascade(label="File", menu=file_menu)
menu_bar.add_cascade(label="Edit", menu=edit_menu)


canvas = Canvas(root)
canvas.pack(fill=BOTH, expand=True)


root.mainloop()
