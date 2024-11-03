import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont
import hashlib
import os
import cv2
import numpy as np
import random
import matplotlib.pyplot as plt

# Forensic Watermark GUI Application
class ForensicWatermarkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Forensic Watermark Encoding & Decoding")
        self.root.geometry("600x400")
        
        self.init_gui()

    def init_gui(self):
        # Encoding Section
        encode_frame = tk.LabelFrame(self.root, text="Encoding Section", padx=10, pady=10)
        encode_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.upload_btn_encode = tk.Button(encode_frame, text="Upload Image for Encoding", command=self.upload_image_for_encoding)
        self.upload_btn_encode.pack(pady=10)

        self.download_btn_encode = tk.Button(encode_frame, text="Download Encoded Image", state="disabled", command=self.download_encoded_image)
        self.download_btn_encode.pack(pady=10)

        # Decoding Section
        decode_frame = tk.LabelFrame(self.root, text="Decoding Section", padx=10, pady=10)
        decode_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.upload_btn_decode = tk.Button(decode_frame, text="Upload Image for Decoding", command=self.upload_image_for_decoding)
        self.upload_btn_decode.pack(pady=10)

        self.preview_label_decode = tk.Label(decode_frame)
        self.preview_label_decode.pack(pady=10)
        
        self.image_path = None
        self.encoded_image = None

    def upload_image_for_encoding(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")])
        if self.image_path:
            try:
                img = cv2.imread(self.image_path)
                height, width, _ = img.shape
                
                # Create unique ID and hash for the image
                image_id = os.path.basename(self.image_path).split(".")[0]
                image_hash = hashlib.md5(img.tobytes()).hexdigest()[:8]

                # Generate random watermark with hash ID
                wm_height, wm_width = 150, 300
                random.seed(2021)
                y_random_indices, x_random_indices = list(range(height)), list(range(width))
                random.shuffle(x_random_indices)
                random.shuffle(y_random_indices)
                random_wm = np.zeros(img.shape, dtype=np.uint8)

                for y in range(wm_height):
                    for x in range(wm_width):
                        if y < len(image_hash) and x < len(image_hash):
                            random_wm[y_random_indices[y], x_random_indices[x]] = ord(image_hash[y % len(image_hash)])

                # Apply watermark to image using FFT
                alpha = 5
                img_f = np.fft.fft2(img)
                result_f = img_f + alpha * random_wm
                result = np.fft.ifft2(result_f)
                result = np.real(result)
                result = result.astype(np.uint8)
                
                # Save encoded image to display later
                self.encoded_image = Image.fromarray(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
                messagebox.showinfo("Success", "Watermark added successfully!")
                self.download_btn_encode.config(state="normal")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to encode image: {e}")

    def download_encoded_image(self):
        if self.encoded_image:
            save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if save_path:
                self.encoded_image.save(save_path)
                messagebox.showinfo("Success", "Encoded image saved successfully!")

    def upload_image_for_decoding(self):
        decode_image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")])
        if decode_image_path:
            try:
                img_ori = cv2.imread(self.image_path)
                img_input = cv2.imread(decode_image_path)
                
                img_ori_f = np.fft.fft2(img_ori)
                img_input_f = np.fft.fft2(img_input)
                alpha = 5
                
                # Extract watermark from the encoded image
                watermark = (img_ori_f - img_input_f) / alpha
                watermark = np.real(watermark).astype(np.uint8)

                # Decode the hash ID from the watermark
                height, width, _ = img_ori.shape
                y_random_indices, x_random_indices = list(range(height)), list(range(width))
                random.seed(2021)
                random.shuffle(x_random_indices)
                random.shuffle(y_random_indices)
                result2 = np.zeros(watermark.shape, dtype=np.uint8)

                for y in range(height):
                    for x in range(width):
                        result2[y, x] = watermark[y_random_indices[y], x_random_indices[x]]
                
                # Display decoded watermark
                decoded_hash = ''.join([chr(result2[y, x][0]) for y in range(8) for x in range(8)])
                messagebox.showinfo("Decoded Hash ID", f"Decoded Hash: {decoded_hash}")

                # Show decoded image preview
                img = Image.fromarray(cv2.cvtColor(img_input, cv2.COLOR_BGR2RGB))
                img.thumbnail((300, 300))
                img_tk = ImageTk.PhotoImage(img)
                self.preview_label_decode.config(image=img_tk)
                self.preview_label_decode.image = img_tk
            except Exception as e:
                messagebox.showerror("Error", f"Failed to decode image: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ForensicWatermarkApp(root)
    root.mainloop()