import tkinter as tk
import os, sys
from PIL import Image, ImageTk

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(base_path, relative_path)

class Controller():
    def __init__(self, changeHatFunction, exitApp):
        self.CHFunction = changeHatFunction
        self.exitApp = exitApp

        self.root = tk.Tk()
        self.root.title("Cat controller")
        self.root.geometry("450x400")
        self.root.configure(bg="black")

        icon_path = resource_path("assets/paws_up.png")
        icon_img = tk.PhotoImage(file=icon_path)
        
        self.root.iconphoto(True, icon_img)

        tk.Label(self.root, text="hats picker", bg="black", fg="white", 
                 font=("Arial", 20, "bold")).pack(side="top")

        self.grid_frame = tk.Frame(self.root, bg="black")
        self.grid_frame.pack(side="top", fill="x", padx=80)

        self.button_paths = [
                ["assets/hats/blank.png", ["None", 0, 0, 0, 0]],
                ["assets/hats/top_hat.png", ["assets/hats/top_hat_rotated.png", 70, 70, 144, -4]],
                ["assets/hats/fedora.png", ["assets/hats/fedora_rotated.png", 100, 100, 130, -4]],
                ["assets/hats/chinese_hat.png", ["assets/hats/chinese_hat_rotated.png", 300, 140, 75, -45]],
                ["assets/hats/dum.png", ["assets/hats/dum_rotated.png", 40, 40, 130, 31]]
            ]
        self.image_refs = []
        
        max_columns = 5  
        
        for i, path in enumerate(self.button_paths):
            try:
                full_img = Image.open(resource_path(path[0]))
                resized_img = full_img.resize((40, 40), Image.Resampling.LANCZOS)
                tk_img = ImageTk.PhotoImage(resized_img)
                self.image_refs.append(tk_img)

                btn = tk.Button(
                    self.grid_frame,
                    image=tk_img,
                    width=40, height=40,
                    bg="#333", borderwidth=0, highlightthickness=0,
                    activebackground="#555",
                    command=lambda p=path[1]: self.CHFunction(p)
                )
                
                row_idx = i // max_columns
                col_idx = i % max_columns
                
                btn.grid(row=row_idx, column=col_idx, padx=10, pady=10)
                
            except Exception as e:
                print(f"Error loading {path}: {e}")

        self.exit_btn = tk.Button(
            self.root, 
            text="Close App", 
            command=self.close,
            bg="#505050", 
            fg="white",
            font=("Arial", 12, "bold"),
            padx=20,
            pady=5
        )
        self.exit_btn.pack(side="top", pady=20)

    def close(self):
        self.exitApp()
        self.root.destroy()