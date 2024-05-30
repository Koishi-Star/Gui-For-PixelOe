import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from pixeloe.pixelize import pixelize


class PixelizeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pixelize Image")
        self.root.geometry("800x600")

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
        self.pixelized_img = None

    def create_widgets(self):
        tk.Label(self.controls_frame, text="Target Size(64-256):").pack(anchor=tk.W)
        self.target_size_entry = tk.Entry(self.controls_frame)
        self.target_size_entry.pack(anchor=tk.W)
        self.target_size_entry.insert(0, "256")

        tk.Label(self.controls_frame, text="Patch Size(4-8):").pack(anchor=tk.W)
        self.patch_size_entry = tk.Entry(self.controls_frame)
        self.patch_size_entry.pack(anchor=tk.W)
        self.patch_size_entry.insert(0, "8")

        tk.Label(self.controls_frame, text="thickness(1-2):").pack(anchor=tk.W)
        self.thickness_entry = tk.Entry(self.controls_frame)
        self.thickness_entry.pack(anchor=tk.W)
        self.thickness_entry.insert(0, "2")

        self.load_button = tk.Button(self.controls_frame, text="Load Image", command=self.load_image)
        self.load_button.pack(fill=tk.X, pady=5)

        self.pixelize_button = tk.Button(self.controls_frame, text="Pixelize", command=self.pixelize_image,
                                         state=tk.DISABLED)
        self.pixelize_button.pack(fill=tk.X, pady=5)

        self.save_button = tk.Button(self.controls_frame, text="Save Image", command=self.save_image, state=tk.DISABLED)
        self.save_button.pack(fill=tk.X, pady=5)

        self.canvas = tk.Canvas(self.canvas_frame, bg='white')
        self.canvas.pack(expand=True, fill=tk.BOTH)

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")])
        if file_path:
            self.img = cv2.imread(file_path)
            self.display_image(self.img)
            self.pixelize_button.config(state=tk.NORMAL)

    def pixelize_image(self):
        target_size = int(self.target_size_entry.get())
        patch_size = int(self.patch_size_entry.get())
        # Fetch additional parameters as needed
        thickness = self.thickness_entry.get()
        # For demonstration, we are only using target_size and patch_size
        self.pixelized_img = pixelize(self.img, target_size=int(target_size),
                                      patch_size=int(patch_size),
                                      thickness=int(thickness))
        self.display_image(self.pixelized_img)
        self.save_button.config(state=tk.NORMAL)

    def save_image(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if file_path:
            cv2.imwrite(file_path, self.pixelized_img)

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
        if self.pixelized_img is not None:
            self.display_image(self.pixelized_img)
        if self.img is not None and self.pixelized_img is None:
            self.display_image(self.img)


if __name__ == "__main__":
    root = tk.Tk()
    app = PixelizeApp(root)
    root.mainloop()
