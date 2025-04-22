import tkinter as tk

def close(window: tk.Tk):
    window.destroy()

def main_window():
    window = tk.Tk()
    window.title("ANM Calculator")
    window.geometry("400x200") 

    window.configure(bg="#f0f0f0")  

    # Botón mejorado
    exit_b = tk.Button(
        window,
        text="Cerrar ventana",
        font=("Helvetica", 14),
        bg="#d9534f",
        fg="white",
        padx=20,
        pady=10,
        command=lambda: close(window)
    )
    exit_b.pack(pady=60)

    window.mainloop()

main_window()
