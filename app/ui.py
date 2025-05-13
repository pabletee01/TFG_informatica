import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os
from app.utils import load_habitat_method
from PIL import Image, ImageTk

C_value = 0.15

# Closing and deleting methods

# Function to clear all widgets inside a frame
def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()
        
# Function to destroy the window
def close(window: tk.Tk):
    window.destroy()
    
# Method to display metrics
def load_metrics_popup(filename, route_metrics):
    if not filename:
        messagebox.showwarning("No selection", "Please select a metrics file.")
        return

    filepath = os.path.join(route_metrics, filename)
    try:
        with open(filepath, "r") as f:
            header = f.readline().strip().split(",")
            values = f.readline().strip().split(",")

        if len(header) != len(values):
            messagebox.showerror("Error", "Mismatch between header and data in metrics file.")
            return

        metrics_text = "\n".join(f"{key}: {val}" for key, val in zip(header, values))
        messagebox.showinfo("Metrics", metrics_text)

    except Exception as e:
        messagebox.showerror("Error", f"Failed to read metrics:\n{str(e)}")

def load_graph_image_popup(filename, route):
    # Checking if a selection has been made
    if not filename:
        messagebox.showwarning("No selection", "Please select a graph image file.")
        return

    # Checking if the introduced file exists
    filepath = os.path.join(route, filename)
    if not os.path.isfile(filepath):
        messagebox.showerror("File not found", f"Could not find: {filepath}")
        return

    # Loading the graph representation (possible improvement)
    try:
        popup = tk.Toplevel()
        popup.title(f"Graph: {filename}")
        popup.configure(bg="#f0f0f0")

        img = Image.open(filepath)
        img = img.resize((1100, 1100), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(img)

        label = tk.Label(popup, image=photo)
        label.image = photo  # Keep reference
        label.pack(padx=10, pady=10)

    except Exception as e:
        messagebox.showerror("Error", f"Failed to open image:\n{str(e)}")

# Methods to load windows

# Command to load habitat widgets
def load_habitat(main_frame):
    # Clear the main frame
    clear_frame(main_frame)

    # Configure the main frame
    main_frame.grid_columnconfigure(0, weight=1)
    main_frame.configure(bg="#f0f0f0")

    # Style configuration for ttk Combobox
    style = ttk.Style()
    style.theme_use('clam')
    style.configure("TCombobox",
                    fieldbackground="white",
                    background="#dfe6e9",
                    font=("Helvetica", 12),
                    padding=5)

    # Title
    title = tk.Label(main_frame,
                     text="Select the input files for ANM analysis",
                     font=("Helvetica", 16, "bold"),
                     bg="#f0f0f0")
    title.grid(row=0, column=0, pady=(30, 10))

    # Habitat selection
    route_habitats = os.getcwd() + "/data/habitats/"
    files_habitats = []
    for _, _, files in os.walk(route_habitats):
        files_habitats.extend(files)

    habitat_frame = tk.Frame(main_frame, bg="#f0f0f0")
    habitat_frame.grid(row=1, column=0, pady=10)

    tk.Label(habitat_frame,
             text="Habitat file:",
             bg="#f0f0f0",
             font=("Helvetica", 12)).pack(anchor="w")

    combo1 = ttk.Combobox(habitat_frame, values=files_habitats, state="readonly", width=60)
    combo1.pack()

    # Configuration selection
    route_config = os.getcwd() + "/config/"
    files_config = []
    for _, _, files in os.walk(route_config):
        files_config.extend(files)

    config_frame = tk.Frame(main_frame, bg="#f0f0f0")
    config_frame.grid(row=2, column=0, pady=10)

    tk.Label(config_frame,
             text="Configuration file:",
             bg="#f0f0f0",
             font=("Helvetica", 12)).pack(anchor="w")

    combo2 = ttk.Combobox(config_frame, values=files_config, state="readonly", width=60)
    combo2.pack()
    
    # Habitat config selection
    route_config = os.getcwd() + "/config_habitat/"
    files_config = []
    for _, _, files in os.walk(route_config):
        files_config.extend(files)

    config_frame = tk.Frame(main_frame, bg="#f0f0f0")
    config_frame.grid(row=3, column=0, pady=10)

    tk.Label(config_frame,
             text="Habitat configuration file:",
             bg="#f0f0f0",
             font=("Helvetica", 12)).pack(anchor="w")

    combo3 = ttk.Combobox(config_frame, values=files_config, state="readonly", width=60)
    combo3.pack()

    # Button row
    button_frame = tk.Frame(main_frame, bg="#f0f0f0")
    button_frame.grid(row=4, column=0, pady=30)

    selected_values = [None, None, None]

    # Continue button
    continue_b = tk.Button(
        button_frame,
        text="Calculate",
        font=("Helvetica", 14),
        bg="#77dd77",
        fg="white",
        command=lambda: on_continue_load_habitat(combo1, combo2, combo3, selected_values, main_frame)
    )
    continue_b.pack(padx=20)

# Command to load the graph representation widgets
def view_habitat(main_frame):
    # Clear the main frame
    clear_frame(main_frame)
    
    # Style configuration for ttk Combobox
    style = ttk.Style()
    style.theme_use('clam')
    style.configure("TCombobox",
                    fieldbackground="white",
                    background="#dfe6e9",
                    font=("Helvetica", 12),
                    padding=5)

    # Configure main frame layout and style
    main_frame.grid_columnconfigure(0, weight=1)
    main_frame.configure(bg="#f0f0f0")

    # Title
    title = tk.Label(main_frame,
                     text="View Habitat",
                     font=("Helvetica", 16, "bold"),
                     bg="#f0f0f0")
    title.grid(row=0, column=0, pady=(30, 10))

    # List metrics files
    route_habitat = os.path.join("data", "graphs")
    files_habitat = []
    for _, _, files in os.walk(route_habitat):
        files_habitat.extend(files)

    # Selection frame
    selection_frame = tk.Frame(main_frame, bg="#f0f0f0")
    selection_frame.grid(row=1, column=0, pady=10)

    tk.Label(selection_frame,
             text="Select habitat graph file:",
             bg="#f0f0f0",
             font=("Helvetica", 12)).pack(anchor="w")

    combo = ttk.Combobox(selection_frame, values=files_habitat, state="readonly", width=60)
    combo.pack()

    # Button frame
    button_frame = tk.Frame(main_frame, bg="#f0f0f0")
    button_frame.grid(row=2, column=0, pady=30)

    load_button = tk.Button(
        button_frame,
        text="Load",
        font=("Helvetica", 14),
        bg="#77dd77",
        fg="white",
        command=lambda: load_graph_image_popup(combo.get(), route_habitat)
    )
    
    load_button.pack()


# Command to load the view metrics widgets
def view_metrics(main_frame):
    # Clear the main frame
    clear_frame(main_frame)
    
    # Style configuration for ttk Combobox
    style = ttk.Style()
    style.theme_use('clam')
    style.configure("TCombobox",
                    fieldbackground="white",
                    background="#dfe6e9",
                    font=("Helvetica", 12),
                    padding=5)

    # Configure main frame layout and style
    main_frame.grid_columnconfigure(0, weight=1)
    main_frame.configure(bg="#f0f0f0")

    # Title
    title = tk.Label(main_frame,
                     text="View Metrics",
                     font=("Helvetica", 16, "bold"),
                     bg="#f0f0f0")
    title.grid(row=0, column=0, pady=(30, 10))

    # List metrics files
    route_metrics = os.path.join("data", "metrics")
    files_metrics = []
    for _, _, files in os.walk(route_metrics):
        files_metrics.extend(files)

    # Selection frame
    selection_frame = tk.Frame(main_frame, bg="#f0f0f0")
    selection_frame.grid(row=1, column=0, pady=10)

    tk.Label(selection_frame,
             text="Select metrics file:",
             bg="#f0f0f0",
             font=("Helvetica", 12)).pack(anchor="w")

    combo = ttk.Combobox(selection_frame, values=files_metrics, state="readonly", width=60)
    combo.pack()

    # Button frame
    button_frame = tk.Frame(main_frame, bg="#f0f0f0")
    button_frame.grid(row=2, column=0, pady=30)

    load_button = tk.Button(
        button_frame,
        text="Load",
        font=("Helvetica", 14),
        bg="#77dd77",
        fg="white",
        command=lambda: load_metrics_popup(combo.get(), route_metrics)
    )
    
    load_button.pack()
    
# Command to modify the C parameter
def set_c_value(main_frame):
    
    global C_value

    # Ask the user for a new value of C
    new_value = simpledialog.askfloat(
        title="Set C Value",
        prompt=f"Current C value is {C_value}\n\nEnter new C value:",
        parent=main_frame,
        minvalue=0.0
    )

    if new_value is not None:
        C_value = new_value
        messagebox.showinfo("Success", f"C value updated to {C_value}")

# Function to execute when clicking "Continue" 
def on_continue_load_habitat(combo1, combo2, combo3, selected_values, main_frame):
    val1 = combo1.get()
    val2 = combo2.get()
    val3 = combo3.get()
    if not val1 or not val2 or not val3:
        messagebox.showwarning("Missing data", "Please select the three files before continuing.")
        return
    selected_values[0] = val1
    selected_values[1] = val2
    selected_values[2] = val3
    
    load_habitat_method(selected_values, C_value)
    messagebox.showinfo("Habitat loaded successfuly", f"Habitat: {val1}\nConfig: {val2}\nHabitat config: {val3}")
    load_habitat(main_frame)

def main_menu():
    menu_window = tk.Tk()
    menu_window.title("ANM Application")
    menu_window.geometry("800x500")
    menu_window.configure(bg="#f0f0f0")

    # Create the main working area
    main_frame = tk.Frame(menu_window, bg="#f0f0f0")
    main_frame.pack(fill="both", expand=True)

    # Menu bar
    menubar = tk.Menu(menu_window, font=("Helvetica", 12), bg="#f0f0f0", fg="black", activebackground="#add8e6", activeforeground="black")

    # File menu
    file_menu = tk.Menu(menubar, tearoff=0, font=("Helvetica", 12), bg="#f0f0f0", fg="black", activebackground="#add8e6", activeforeground="black")
    # Commands for each window.
    file_menu.add_command(label="Load Habitat", command=lambda: load_habitat(main_frame))
    file_menu.add_command(label="View Habitat", command=lambda: view_habitat(main_frame))
    file_menu.add_command(label="View Metrics", command=lambda: view_metrics(main_frame))
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=lambda: close(menu_window))
    # Commands for options
    options_menu = tk.Menu(menubar, tearoff=0, font=("Helvetica", 12), bg="#f0f0f0", fg="black", activebackground="#add8e6", activeforeground="black")
    options_menu.add_command(label="C parameter", command=lambda: set_c_value(main_frame))

    menubar.add_cascade(label="Window", menu=file_menu)
    menubar.add_cascade(label="Options", menu=options_menu)

    # Attach menu bar
    menu_window.config(menu=menubar)

    menu_window.mainloop()
