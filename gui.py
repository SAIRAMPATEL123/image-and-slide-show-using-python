import os
import tkinter as tk
from tkinter import LEFT, RIGHT, Button, Label

import cv2
from PIL import Image, ImageTk

from camera import Camera


class CameraApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Camera and Slideshow App")

        # Frame for camera and its button
        self.camera_frame = tk.Frame(self.root)
        self.camera_frame.pack(side=LEFT, padx=10, pady=10)

        # Camera related
        self.camera = Camera()
        self.camera_label = Label(self.camera_frame)
        self.camera_label.pack()

        # Capture button
        self.capture_button = Button(self.camera_frame, text="Capture Photo", command=self.capture_photo)
        self.capture_button.pack()

        # Frame for slideshow and its buttons
        self.slideshow_frame = tk.Frame(self.root)
        self.slideshow_frame.pack(side=RIGHT, padx=10, pady=10)

        # Slideshow related
        self.slideshow_label = Label(self.slideshow_frame)
        self.slideshow_label.pack()

        # Buttons to control the slideshow
        self.prev_button = Button(self.slideshow_frame, text="<< Prev", command=self.prev_image)
        self.prev_button.pack(side=LEFT, padx=5)

        self.next_button = Button(self.slideshow_frame, text="Next >>", command=self.next_image)
        self.next_button.pack(side=RIGHT, padx=5)

        self.image_list = []
        self.image_index = 0
        self.load_images_from_folder(r'C:\Users\sai\camera_gui_app\images')  # Specify your folder path here

        # Start updating frames
        self.update_camera_frame()
        self.update_slideshow_frame()

    def load_images_from_folder(self, folder):
        """Load images from the specified folder."""
        valid_extensions = (".jpg", ".jpeg", ".png", ".gif")
        self.image_list = [os.path.join(folder, f) for f in os.listdir(folder) if f.lower().endswith(valid_extensions)]
        if not self.image_list:
            print("No images found in folder")

    def update_camera_frame(self):
        frame = self.camera.get_frame()
        if frame is not None:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=image)
            self.camera_label.imgtk = imgtk
            self.camera_label.configure(image=imgtk)
        self.root.after(10, self.update_camera_frame)

    def update_slideshow_frame(self):
        if self.image_list:
            image_path = self.image_list[self.image_index]
            image = Image.open(image_path)
            image = image.resize((640, 480), Image.Resampling.LANCZOS)  # Use LANCZOS for high-quality downsampling
            imgtk = ImageTk.PhotoImage(image=image)
            self.slideshow_label.imgtk = imgtk
            self.slideshow_label.configure(image=imgtk)

    def next_image(self):
        if self.image_list:
            self.image_index = (self.image_index + 1) % len(self.image_list)
            self.update_slideshow_frame()

    def prev_image(self):
        if self.image_list:
            self.image_index = (self.image_index - 1) % len(self.image_list)
            self.update_slideshow_frame()

    def capture_photo(self):
        frame = self.camera.get_frame()
        if frame is not None:
            # Convert the frame to RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Ensure the save path has a valid file extension
            save_path = r'C:\Users\sai\camera_gui_app\captured_images\captured_image.jpg'  # Specify your save path here
            # Save the image
            Image.fromarray(frame).save(save_path, format='JPEG')
            print(f"Photo captured and saved at {save_path}")

    def run(self):
        self.root.mainloop()

    def __del__(self):
        self.camera.release()
