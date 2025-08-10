import tkinter as tk
from tkinter import filedialog, messagebox
from src import inference
import os

class SimpleUI:
    def __init__(self, root):
        self.root = root
        root.title("Poster Replacer Simple UI")

        self.label = tk.Label(root, text="Select your photo:")
        self.label.pack()

        self.select_btn = tk.Button(root, text="Browse...", command=self.browse_image)
        self.select_btn.pack()

        self.run_btn = tk.Button(root, text="Generate Poster", command=self.run_pipeline, state=tk.DISABLED)
        self.run_btn.pack()

        self.user_img_path = ''
        self.posters_dir = os.path.join('data', 'posters')
        self.annotations_dir = os.path.join('data', 'annotations')
        self.output_dir = os.path.join('data', 'outputs')

    def browse_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.png;*.jpeg")])
        if path:
            self.user_img_path = path
            self.run_btn.config(state=tk.NORMAL)

    def run_pipeline(self):
        try:
            output_path = inference.run_pipeline(self.user_img_path, self.posters_dir, self.annotations_dir, self.output_dir)
            messagebox.showinfo("Success", f"Poster generated at {output_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleUI(root)
    root.mainloop()
