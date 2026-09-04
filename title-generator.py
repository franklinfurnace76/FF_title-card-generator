import os
import sys
import shutil
import subprocess
import tkinter as tk
from tkinter import messagebox

# Path to ImageMagick convert tool
IMAGEMAGICK_PATH = "/opt/local/bin/convert"

OUTPUT_DIR = os.path.join(os.path.expanduser("~"), "Desktop", "Titlecards")
os.makedirs(OUTPUT_DIR, exist_ok=True)

#--------------------------
#Paths setup
#-----------------------
if getattr(sys, 'frozen', False):
    # Running as PyInstaller executable
    BASE_DIR = sys._MEIPASS
else:
    # Running as normal Python script
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ASSETS_DIR = os.path.join(BASE_DIR, "assets")

# Assets
title_template = os.path.join(ASSETS_DIR, "template_titlecard.png")
ff_logo_path = os.path.join(ASSETS_DIR, "ff_logo.png")
font_path = os.path.join(ASSETS_DIR, "ArialNarrowBold.ttf")

#-------------------------
#GUI setup
#--------------------------

root = tk.Tk()
root.title("Titlecard-Generator")
root.configure(background="#969696")

root.minsize(200, 200)
root.maxsize(500, 550)
root.geometry("500x550+50+50")

#Top frame
top_frame = tk.Frame(root, height=20, bg="#969696")
top_frame.pack(padx=5, pady=5, anchor="n", fill="x")

#logo
ff_logo = tk.Frame(top_frame, width=20, height=20, bg="#d6d6d6")
ff_logo.grid(row=0, column=0, rowspan=2, padx=5, pady=5)

try:
    ff_logo_image = tk.PhotoImage(file=ff_logo_path).subsample(10, 10)
    tk.Label(ff_logo, image=ff_logo_image).pack(padx=5, pady=5)
except Exception:
    pass # if logo doesn't exist - case

# headings
heading_title = tk.Label(top_frame, text="Title-Generator", font=("Arial", 32), fg="#ffffff", bg="#969696")
heading_title.grid(row=0, column=1, padx=3, pady=3)
heading_subtitle = tk.Label(top_frame, text="Created by Franklin Furnace", font=("Arial", 16), fg="#ffffff", bg="#969696")
heading_subtitle.grid(row=1, column=1, padx=3, pady=3)

# GUI frame
main_frame = tk.Frame(root, bg="#969696")
main_frame.pack(padx=5, pady=10, fill="both", expand=True)

# Artist name ---
question1 = tk.Label(main_frame, text="Enter Artist Name", font=("Arial", 16), bg="#d6d6d6")
question1.pack(padx=3, pady=3, anchor="nw")
answer1_var = tk.StringVar()
answer1 = tk.Entry(main_frame, textvariable=answer1_var, font=('Arial', 20), bg="#ffffff", fg="#000000")
answer1.pack(padx=3, pady=3, anchor="nw")

#Performance title ---
question2 = tk.Label(main_frame, text="Enter Performance Title", font=("Arial", 16), bg="#d6d6d6")
question2.pack(padx=3, pady=3, anchor="nw")
answer2_var = tk.StringVar()
answer2 = tk.Entry(main_frame, textvariable=answer2_var, font=('Arial', 20), bg="#ffffff", fg="#000000")
answer2.pack(padx=3, pady=3, anchor="nw")

#Sub-title ---
question_sub = tk.Label(main_frame, text="Enter Sub-title (Optional)", font=("Arial", 16), bg="#d6d6d6")
question_sub.pack(padx=3, pady=3, anchor="nw")
answer_sub_var = tk.StringVar()
answer_sub = tk.Entry(main_frame, textvariable=answer_sub_var, font=('Arial', 20), bg="#ffffff", fg="#000000")
answer_sub.pack(padx=3, pady=3, anchor="nw")

#Performance Year ---
question3 = tk.Label(main_frame, text="Enter Performance Year", font=("Arial", 16), bg="#d6d6d6")
question3.pack(padx=3, pady=3, anchor="nw")
answer3_var = tk.StringVar()
answer3 = tk.Entry(main_frame, textvariable=answer3_var, font=('Arial', 20), bg="#ffffff", fg="#000000")
answer3.pack(padx=3, pady=3, anchor="nw")

#--------------------------
#Generate button
#-------------------------
def on_button_click():
    print("Button clicked!")

    #retreieve inputs
    entered1 = answer1_var.get().strip() 
    entered2 = answer2_var.get().strip() 
    entered_sub = answer_sub_var.get().strip() 
    entered3 = answer3_var.get().strip() 

    #validation of fields
    if not entered1 or not entered2 or not entered3:
        messagebox.showerror("Error", "Please fill in Artist, Title, and Year.")
        return

    #filename
    safe_filename = f"{entered1}_{entered2}_{entered3}".replace(" ", "_")
    output_file = os.path.join(OUTPUT_DIR, f"{safe_filename}.jpg")

    #imagemagick command
    cmd = [
        IMAGEMAGICK_PATH,
        title_template,

        "-pointsize", "85",
        "-font", font_path,
        "-fill", "white",
        "-annotate", "+900+540", entered1,

        "-pointsize", "60",
        "-font", font_path,
        "-fill", "white",
        "-annotate", "+900+630", entered2,

        "-pointsize", "50",          
        "-font", font_path,
        "-fill", "white",
        "-annotate", "+900+700", entered_sub, 

        "-pointsize", "72",
        "-font", font_path,
        "-fill", "white",
        "-annotate", "+900+820", entered3,

        output_file
    ]

    try:
        subprocess.run(cmd, check=True)
        messagebox.showinfo("Success", f"Titlecard generated:\n{output_file}")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"ImageMagick failed:\n{e}")
    except FileNotFoundError:
        messagebox.showerror("Error", f"ImageMagick not found. Check path:\n{IMAGEMAGICK_PATH}")

# Generate button
confirm_btn = tk.Button(main_frame, text="Generate", command=on_button_click, height=2, width=30)
confirm_btn.pack(pady=20, padx=20, anchor="nw")

root.mainloop()
