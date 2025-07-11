import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np

class BMPViewerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("BMP File Viewer")
        
        self.canvas_size = 600  # canvas size for image display
        self.display_frame = tk.Frame(master)
        self.display_frame.pack()
        
        self.canvas = tk.Canvas(self.display_frame, width=self.canvas_size, height=self.canvas_size) #creating a canvas to display the image
        self.canvas.pack()
        
        # Rest of your original GUI elements
        self.open_button = tk.Button(master, text="Open BMP File", command=self.open_file)
        self.open_button.pack()

        self.metadata_label = tk.Label(master, text="")
        self.metadata_label.pack()

        self.updated_metadata_label = tk.Label(master, text="")
        self.updated_metadata_label.pack()

        # Control panel frame
        self.control_frame = tk.Frame(master)
        self.control_frame.pack(side="bottom", fill="x")

        self.brightness_slider = tk.Scale(self.control_frame, from_=0, to=100, orient=tk.HORIZONTAL,
                                        label="Brightness", command=self.update_image)
        self.brightness_slider.set(100)
        self.brightness_slider.pack(side="left", fill="x", expand=True)

        self.scale_slider = tk.Scale(self.control_frame, from_=0, to=100, orient=tk.HORIZONTAL,
                                    label="Scale (%)", command=self.update_image)
        self.scale_slider.set(100)
        self.scale_slider.pack(side="left", fill="x", expand=True)

        # RGB buttons
        self.r_button = tk.Button(self.control_frame, text="Toggle Red", command=self.toggle_red)
        self.r_button.pack(side="left")
        self.g_button = tk.Button(self.control_frame, text="Toggle Green", command=self.toggle_green)
        self.g_button.pack(side="left")
        self.b_button = tk.Button(self.control_frame, text="Toggle Blue", command=self.toggle_blue)
        self.b_button.pack(side="left")

        self.show_red = self.show_green = self.show_blue = True
        self.original_width = self.original_height = 0
        self.base_scale = 1.0
    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("BMP files", "*.bmp")])
        if file_path:
            try:
                with open(file_path, "rb") as f:
                    bmp_bytes = f.read()
                    self.validate_bmp(bmp_bytes)
                    self.parse_bmp(bmp_bytes)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file:\n{str(e)}")

    def validate_bmp(self, bmp_bytes):
        if len(bmp_bytes) < 54:
            raise ValueError("Not a valid BMP file (header too small)")
        if bmp_bytes[0] != ord('B') or bmp_bytes[1] != ord('M'):
            raise ValueError("Not a valid BMP file (missing BM header)")

    def parse_bmp(self, bmp_bytes):
        self.original_file_size = int.from_bytes(bmp_bytes[2:6], 'little')
        self.original_width = int.from_bytes(bmp_bytes[18:22], 'little')
        self.original_height = int.from_bytes(bmp_bytes[22:26], 'little')
        bpp = int.from_bytes(bmp_bytes[28:30], 'little')

        self.metadata_label.config(
            text=f"Original: file_size {self.original_file_size}, Width: {self.original_width}, Hight: {self.original_height}, BPP: {bpp}"
        )
        self.display_image(bmp_bytes)

    def display_image(self, bmp_bytes):
        bpp = int.from_bytes(bmp_bytes[28:30], 'little')
        width, height = self.original_width, self.original_height

        if bpp == 24:
            self.image_array = self.parse_24bit(bmp_bytes, width, height)
        elif bpp == 1:
            self.image_array = self.parse_1bit(bmp_bytes, width, height)
        elif bpp == 4:
            self.image_array = self.parse_4bit(bmp_bytes, width, height)
        elif bpp == 8:
            self.image_array = self.parse_8bit(bmp_bytes, width, height)
        else:
            raise ValueError(f"Unsupported BPP: {bpp}")

        # Calculating initial scale to fit in square
        self.base_scale = min(self.canvas_size/width, self.canvas_size/height) # The minimum scale factor to fit the image in the canvas and the scalling will be done based on this factor
        self.update_image()
    def parse_24bit(self, bmp_bytes, width, height):
        pixel_data = bmp_bytes[54:]
        row_size = (width * 3 + 3) & ~3
        image_array = np.zeros((height, width, 3), dtype=np.uint8)

        for y in range(height):
            for x in range(width):
                offset = y * row_size + x * 3
                if offset + 2 < len(pixel_data):
                    b, g, r = pixel_data[offset:offset + 3]
                    image_array[y, x] = [r, g, b]
        return image_array

    def parse_1bit(self, bmp_bytes, width, height):
        # Offset to the pixel data
        pixel_data_offset = int.from_bytes(bmp_bytes[10:14], 'little')
        pixel_data = bmp_bytes[pixel_data_offset:]

        color_table = bmp_bytes[54:62]
        colors = [
            (color_table[i + 2], color_table[i + 1], color_table[i])
            for i in range(0, len(color_table), 4)
        ]

        row_size = (width + 31) // 32 * 4
        image_array = np.zeros((height, width, 3), dtype=np.uint8)

        for y in range(height):
            row_start = y * row_size
            for x in range(width):
                byte_index = row_start + (x // 8)
                bit_index = 7 - (x % 8)
                if byte_index < len(pixel_data):
                    pixel_value = (pixel_data[byte_index] >> bit_index) & 1
                    image_array[y, x] = colors[pixel_value]

        return image_array

    def parse_4bit(self, bmp_bytes, width, height):
        # Offset to the pixel data
        pixel_data_offset = int.from_bytes(bmp_bytes[10:14], 'little')
        pixel_data = bmp_bytes[pixel_data_offset:]

        color_table_size = 16 * 4
        color_table = bmp_bytes[54:54 + color_table_size]
        colors = [
            (color_table[i + 2], color_table[i + 1], color_table[i])
            for i in range(0, len(color_table), 4)
        ]

        row_size = (width + 7) // 8 * 4
        image_array = np.zeros((height, width, 3), dtype=np.uint8)

        for y in range(height):
            row_start = y * row_size
            for x in range(width):
                byte_index = row_start + (x // 2)
                if byte_index < len(pixel_data):
                    if x % 2 == 0:
                        pixel_value = (pixel_data[byte_index] >> 4) & 0x0F
                    else:
                        pixel_value = pixel_data[byte_index] & 0x0F
                    image_array[y, x] = colors[pixel_value]

        return image_array

    def parse_8bit(self, bmp_bytes, width, height):
        # Offset to the pixel data
        pixel_data_offset = int.from_bytes(bmp_bytes[10:14], 'little')
        pixel_data = bmp_bytes[pixel_data_offset:]

        color_table_size = 256 * 4
        color_table = bmp_bytes[54:54 + color_table_size]
        colors = [
            (color_table[i + 2], color_table[i + 1], color_table[i])
            for i in range(0, len(color_table), 4)
        ]

        row_size = (width + 3) // 4 * 4
        image_array = np.zeros((height, width, 3), dtype=np.uint8)

        for y in range(height):
            row_start = y * row_size
            for x in range(width):
                byte_index = row_start + x
                if byte_index < len(pixel_data):
                    pixel_value = pixel_data[byte_index]
                    image_array[y, x] = colors[pixel_value]

        return image_array
    def update_image(self, event=None):
        if not hasattr(self, 'image_array'):
            return

        user_scale = self.scale_slider.get() / 100
        combined_scale = self.base_scale * user_scale

        new_width = int(self.original_width * combined_scale)
        new_height = int(self.original_height * combined_scale)
        
        # Applying brightness
        adjusted = np.clip(self.image_array * (self.brightness_slider.get()/100), 0, 255)
        
        scaled = np.zeros((new_height, new_width, 3), dtype=np.uint8) # Creating a new array to store the scaled image
        for y in range(new_height):
            for x in range(new_width):
                orig_y = min(int(y/combined_scale), self.original_height-1)
                orig_x = min(int(x/combined_scale), self.original_width-1)
                scaled[y, x] = adjusted[orig_y, orig_x]

        self.photo_image = tk.PhotoImage(width=new_width, height=new_height)
        for y in range(new_height):
            for x in range(new_width):
                r, g, b = scaled[y, x]
                r = r if self.show_red else 0
                g = g if self.show_green else 0
                b = b if self.show_blue else 0
                self.photo_image.put(f"#{r:02x}{g:02x}{b:02x}", (x, new_height - 1 - y))

        # Clearing canvas and center image
        self.canvas.delete("all")
        x_pos = (self.canvas_size - new_width) // 2
        y_pos = (self.canvas_size - new_height) // 2
        self.canvas.create_image(x_pos, y_pos, anchor=tk.NW, image=self.photo_image)

        self.updated_metadata_label.config(
            text=f"Display Size: {new_width}x{new_height} | Zoom: {self.scale_slider.get()}%"
        )
    def toggle_red(self):
        self.show_red = not self.show_red
        self.update_image()

    def toggle_green(self):
        self.show_green = not self.show_green
        self.update_image()

    def toggle_blue(self):
        self.show_blue = not self.show_blue
        self.update_image()
if __name__ == "__main__":
    root = tk.Tk()
    app = BMPViewerApp(root)
    root.mainloop()