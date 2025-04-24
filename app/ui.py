import tkinter as tk
from tkinter import ttk, messagebox
import os

# Function to close the window
def close(window: tk.Tk):
    window.destroy()

# Function to execute when clicking "Continue"
def on_continue(combo1, combo2, window, selected_values):
    val1 = combo1.get()
    val2 = combo2.get()
    if not val1 or not val2:
        messagebox.showwarning("Missing data", "Please select both files before continuing.")
        return
    selected_values[0] = val1
    selected_values[1] = val2
    window.destroy()

# Main interface window
def main_window():
    window = tk.Tk()
    window.title("ANM Calculator")
    window.geometry("800x500")
    window.configure(bg="#f0f0f0")

    # Configure column for centering content
    window.grid_columnconfigure(0, weight=1)

    # Style for ttk Combobox
    style = ttk.Style()
    style.theme_use('clam')
    style.configure("TCombobox",
                    fieldbackground="white",
                    background="#dfe6e9",
                    font=("Helvetica", 12),
                    padding=5)

    # Title
    title = tk.Label(window,
                     text="Select the input files for ANM analysis",
                     font=("Helvetica", 16, "bold"),
                     bg="#f0f0f0")
    title.grid(row=0, column=0, pady=(30, 10))

    # Habitat selection
    route_habitats = os.getcwd() + "/data/habitats/"
    files_habitats = []
    for _, _, files in os.walk(route_habitats):
        files_habitats.extend(files)

    habitat_frame = tk.Frame(window, bg="#f0f0f0")
    habitat_frame.grid(row=1, column=0, pady=10)
    tk.Label(habitat_frame, text="Habitat file:", bg="#f0f0f0", font=("Helvetica", 12)).pack(anchor="w")
    combo1 = ttk.Combobox(habitat_frame, values=files_habitats, state="readonly", width=60)
    combo1.pack()

    # Configuration selection
    route_config = os.getcwd() + "/config/"
    files_config = []
    for _, _, files in os.walk(route_config):
        files_config.extend(files)

    config_frame = tk.Frame(window, bg="#f0f0f0")
    config_frame.grid(row=2, column=0, pady=10)
    tk.Label(config_frame, text="Configuration file:", bg="#f0f0f0", font=("Helvetica", 12)).pack(anchor="w")
    combo2 = ttk.Combobox(config_frame, values=files_config, state="readonly", width=60)
    combo2.pack()

    # Button row
    button_frame = tk.Frame(window, bg="#f0f0f0")
    button_frame.grid(row=3, column=0, pady=30)

    selected_values = [None, None]

    exit_b = tk.Button(
        button_frame,
        text="Close",
        font=("Helvetica", 14),
        bg="#d9534f",
        fg="white",
        command=lambda: close(window)
    )
    exit_b.pack(side="left", padx=20)

    continue_b = tk.Button(
        button_frame,
        text="Calculate",
        font=("Helvetica", 14),
        bg="#77dd77",
        fg="white",
        command=lambda: on_continue(combo1, combo2, window, selected_values)
    )
    continue_b.pack(side="right", padx=20)

    window.mainloop()
    return selected_values
