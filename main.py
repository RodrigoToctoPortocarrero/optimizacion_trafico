# main.py
import tkinter as tk
from gui.main_window import MainWindow
from config import Config

def main():
    # Crear la ventana principal
    root = tk.Tk()
    
    # Crear la aplicación pasando root
    app = MainWindow(root)
    
    # Iniciar el bucle principal de Tkinter
    root.mainloop()

if __name__ == "__main__":
    main()