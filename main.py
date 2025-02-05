import tkinter as tk
from tkinter import ttk, PhotoImage
import requests
from PIL import Image, ImageTk
import json
import os

# Let's a directory for flags if it doesn't exist
if not os.path.exists('flags'):
    os.makedirs('flags')

def fetch_flag(country_code):
    url = f"https://flagcdn.com/256x192/{country_code.lower()}.png"
    file_path = f'flags/{country_code}.png'
    if not os.path.exists(file_path):
        response = requests.get(url)
        if response.status_code == 200:
            with open(file_path, 'wb') as f:
                f.write(response.content)
    return file_path

def display_flags(root, countries):
    # Frame for holding the flags with scrollbars
    flag_frame = ttk.Frame(root)
    flag_frame.pack(fill=tk.BOTH, expand=True)

    canvas = tk.Canvas(flag_frame)
    scrollbar = ttk.Scrollbar(flag_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Constants for flag size
    FLAG_WIDTH = 256
    FLAG_HEIGHT = 192  # Maintain 4:3 aspect ratio

    for idx, country in enumerate(countries):
        flag_path = fetch_flag(country)
        img = Image.open(flag_path)
        
        # Resize image to maintain aspect ratio but fit within specified dimensions
        img_resized = img.resize((FLAG_WIDTH, FLAG_HEIGHT), Image.LANCZOS)
        photo = ImageTk.PhotoImage(img_resized)
        
        label = ttk.Label(scrollable_frame, image=photo)
        label.image = photo  # keep a reference!
        label.grid(row=idx // 5, column=idx % 5, padx=5, pady=5, sticky="nsew")  # Wrap every 5 flags

    # Configure grid to expand equally
    for i in range(5):
        scrollable_frame.grid_columnconfigure(i, weight=1)

def main():
    root = tk.Tk()
    root.title("Country Flags")
    with open('./data/country_codes.json') as f:
        countries = json.load(f)
        print(f"Flags for all country codes:\n{countries}")
    display_flags(root, countries)
    
    # Set window size
    root.geometry("1400x400")
    root.mainloop()

if __name__ == "__main__":
    main()