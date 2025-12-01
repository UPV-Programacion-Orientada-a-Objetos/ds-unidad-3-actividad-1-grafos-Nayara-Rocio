"""
NeuroNet - Sistema de Análisis y Visualización de Propagación en Redes Masivas
"""

import tkinter as tk
from neuronet_gui import NeuroNetGUI

def main():
    print("=== NeuroNet - Sistema de Análisis de Redes Masivas ===")
    print("Inicializando interfaz gráfica...")
    
    root = tk.Tk()
    app = NeuroNetGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()