import cv2
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageEnhance
from pixeloe.pixelize import pixelize
import numpy as np


# noinspection PyAttributeOutsideInit
class PixelizeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pixelize Image(Recommend Using Default Parameter)")
        self.root.geometry("800x600")

        self.label = tk.Label(self.root)
        self.label.pack()

        # Frame for controls
        self.controls_frame = tk.Frame(self.root)
        self.controls_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        # Frame for canvas
        self.canvas_frame = tk.Frame(self.root)
        self.canvas_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

        self.create_widgets()

        # Bind resize event
        self.root.bind("<Configure>", self.on_resize)

        self.img = None
        self.ori_img = None

    def create_widgets(self):
        tk.Label(self.controls_frame, text="Target Size(64-256):").pack(anchor=tk.W)
        self.target_size_entry = tk.Entry(self.controls_frame)
        self.target_size_entry.pack(anchor=tk.W)
        self.target_size_entry.insert(0, "256")

        tk.Label(self.controls_frame, text="Patch Size(4-8):").pack(anchor=tk.W)
        self.patch_size_entry = tk.Entry(self.controls_frame)
        self.patch_size_entry.pack(anchor=tk.W)
        self.patch_size_entry.insert(0, "8")

        tk.Label(self.controls_frame, text="Thickness(1-2):").pack(anchor=tk.W)
        self.thickness_entry = tk.Entry(self.controls_frame)
        self.thickness_entry.pack(anchor=tk.W)
        self.thickness_entry.insert(0, "1")

        # tk.Label(self.controls_frame, text="Detected Pixels(1-8):").pack(anchor=tk.W)
        # self.detected_piexls_entry = tk.Entry(self.controls_frame)
        # self.detected_piexls_entry.pack(anchor=tk.W)
        # self.detected_piexls_entry.insert(0, "4")

        tk.Label(self.controls_frame, text="Add Contrast(0.1-5.0):").pack(anchor=tk.W)
        self.add_contrast_entry = tk.Entry(self.controls_frame)
        self.add_contrast_entry.pack(anchor=tk.W)
        self.add_contrast_entry.insert(0, "1.1")

        self.load_button = tk.Button(self.controls_frame, text="Load Image", command=self.load_image)
        self.load_button.pack(fill=tk.X, pady=5)

        self.add_contrast_default_button = tk.Button(self.controls_frame, text="Add Contrast Default",
                                                     command=self.add_contrast_default, state=tk.DISABLED)
        self.add_contrast_default_button.pack(fill=tk.X, pady=5)

        self.add_contrast_button = tk.Button(self.controls_frame, text="Add Contrast",
                                             command=self.add_contrast, state=tk.DISABLED)
        self.add_contrast_button.pack(fill=tk.X, pady=5)

        self.pixelize_button = tk.Button(self.controls_frame, text="Pixelize", command=self.pixelize_image,
                                         state=tk.DISABLED)
        self.pixelize_button.pack(fill=tk.X, pady=5)

        # self.replace_button = tk.Button(self.controls_frame, text="Replace Pixel",
        #                                 command=self.detect_and_replace_pixels, state=tk.DISABLED)
        # self.replace_button.pack(fill=tk.X, pady=5)

        tk.Label(self.controls_frame, text="Palette Mode:").pack(anchor=tk.W)
        self.palette_var = tk.StringVar(self.controls_frame)
        self.palette_combobox = ttk.Combobox(self.controls_frame, textvariable=self.palette_var,
                                             values=["ADAPTIVE", "WEB", "Black and White"])
        self.palette_combobox.pack(anchor=tk.W)
        self.palette_combobox.current(0)

        tk.Label(self.controls_frame, text="Max Colors(recommend16-64):").pack(anchor=tk.W)
        self.colors_var = tk.IntVar(self.controls_frame)
        self.colors_combobox = ttk.Combobox(self.controls_frame, textvariable=self.colors_var,
                                            values=[2, 4, 8, 16, 32, 64, 128, 256])
        self.colors_combobox.pack(anchor=tk.W)
        self.colors_combobox.current(4)

        self.convert_button = tk.Button(self.controls_frame, text="Convert To 8bit Color",
                                        command=self.convert_to_8bit_color, state=tk.DISABLED)
        self.convert_button.pack(fill=tk.X, pady=5)

        self.clear_button = tk.Button(self.controls_frame, text="Clear Canvas",
                                      command=self.clear_canvas, state=tk.DISABLED)
        self.clear_button.pack(fill=tk.X, pady=5)

        self.recover_original_img_button = tk.Button(self.controls_frame, text="Recover Original Img",
                                                     command=self.recover_original_img, state=tk.DISABLED)
        self.recover_original_img_button.pack(fill=tk.X, pady=5)

        self.save_button = tk.Button(self.controls_frame, text="Save Image", command=self.save_image, state=tk.DISABLED)
        self.save_button.pack(fill=tk.X, pady=5)

        self.canvas = tk.Canvas(self.canvas_frame, bg='white')
        self.canvas.pack(expand=True, fill=tk.BOTH)

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")])
        if file_path:
            self.img = cv2.imread(file_path)
            self.ori_img = self.img
            self.display_image(self.img)
            self.pixelize_button.config(state=tk.NORMAL)
            self.convert_button.config(state=tk.NORMAL)
            self.clear_button.config(state=tk.NORMAL)
            self.recover_original_img_button.config(state=tk.NORMAL)
            self.add_contrast_button.config(state=tk.NORMAL)
            self.add_contrast_default_button.config(state=tk.NORMAL)

    def add_contrast_default(self):
        img_yuv = np.array(Image.fromarray(cv2.cvtColor(np.array(self.img), cv2.COLOR_BGR2YUV)))
        img_yuv[:, :, 0] = cv2.equalizeHist(img_yuv[:, :, 0])
        self.img = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)
        self.display_image(self.img)
        self.save_button.config(state=tk.NORMAL)

    def pixelize_image(self):
        target_size = int(self.target_size_entry.get())
        patch_size = int(self.patch_size_entry.get())
        thickness = int(self.thickness_entry.get())
        self.img = pixelize(self.img, target_size=target_size, patch_size=patch_size, thickness=thickness)
        self.display_image(self.img)
        self.save_button.config(state=tk.NORMAL)

    def add_contrast(self):
        contrast_factor = float(self.add_contrast_entry.get())
        img_pil = Image.fromarray(cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB))
        enhancer = ImageEnhance.Contrast(img_pil)
        img_enhanced = enhancer.enhance(contrast_factor)
        self.img = cv2.cvtColor(np.array(img_enhanced), cv2.COLOR_RGB2BGR)
        self.display_image(self.img)
        self.save_button.config(state=tk.NORMAL)

    def detect_and_replace_pixels(self):
        # Ensure detected_pixels_entry returns an integer
        detected_pixels_threshold = int(self.detected_piexls_entry.get())

        # Convert BGR image to RGB for PIL processing
        img_pil = Image.fromarray(cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB))
        pixels = img_pil.load()
        width, height = img_pil.size
        new_image = img_pil.copy()
        new_pixels = new_image.load()

        for x in range(width):
            for y in range(height):
                current_pixel = pixels[x, y]
                same_color_count = 0
                neighbors = [
                    (i, j) for i in range(-1, 2) for j in range(-1, 2)
                    if (i, j) != (0, 0)
                ]

                for i, j in neighbors:
                    if 0 <= x + i < width and 0 <= y + j < height:
                        if pixels[x + i, y + j] == current_pixel:
                            same_color_count += 1
                if same_color_count >= detected_pixels_threshold:
                    new_pixels[x, y] = current_pixel

        # Convert back to BGR format for OpenCV
        self.img = cv2.cvtColor(np.array(new_image), cv2.COLOR_RGB2BGR)
        self.display_image(self.img)
        self.save_button.config(state=tk.NORMAL)

    def save_image(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if file_path:
            cv2.imwrite(file_path, self.img)

    def convert_to_8bit_color(self):

        palette_mode = self.palette_var.get()
        colors = self.colors_var.get()

        self.convert_button.config(state=tk.ACTIVE)
        img_pil = Image.fromarray(cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB))
        if palette_mode == "ADAPTIVE":
            img_8bit = img_pil.convert("P", palette=Image.ADAPTIVE, colors=colors)
        if palette_mode == "WEB":
            img_8bit = img_pil.convert("P", palette=Image.WEB)
        if palette_mode == "Black and White":
            img_8bit = img_pil.convert("1")
        self.img = cv2.cvtColor(np.array(img_8bit.convert("RGB")), cv2.COLOR_BGR2RGB)
        self.display_image(self.img)
        self.save_button.config(state=tk.NORMAL)

    def display_image(self, img):
        self.canvas.delete("all")
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)

        # Resize image to fit the canvas
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        img_pil.thumbnail((canvas_width, canvas_height), Image.Resampling.LANCZOS)

        img_tk = ImageTk.PhotoImage(image=img_pil)
        self.canvas.create_image(canvas_width // 2, canvas_height // 2, image=img_tk, anchor=tk.CENTER)
        self.canvas.image = img_tk

    def on_resize(self, event):
        if self.img is not None:
            self.display_image(self.img)

    def clear_canvas(self):
        if self.img is not None:
            self.img = None
            self.canvas.delete("all")
            self.pixelize_button.config(state=tk.DISABLED)
            self.convert_button.config(state=tk.DISABLED)
            self.clear_button.config(state=tk.DISABLED)
            self.save_button.config(state=tk.DISABLED)
            self.add_contrast_button.config(state=tk.DISABLED)
            self.add_contrast_default_button.config(state=tk.DISABLED)

    def recover_original_img(self):
        if self.ori_img is not None:
            self.img = self.ori_img
            self.display_image(self.img)
            self.pixelize_button.config(state=tk.NORMAL)
            self.convert_button.config(state=tk.NORMAL)
            self.clear_button.config(state=tk.NORMAL)
            self.save_button.config(state=tk.NORMAL)
            self.add_contrast_button.config(state=tk.NORMAL)
            self.add_contrast_default_button.config(state=tk.NORMAL)


if __name__ == "__main__":
    root = tk.Tk()
    app = PixelizeApp(root)
    root.mainloop()
