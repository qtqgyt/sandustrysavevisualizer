#!python
from loguru import logger
import sys
import tkinter as tk
from tkinter import filedialog

from map import Map
from window import window

@logger.catch
def main():
    if len(sys.argv) > 1:
        json_path = sys.argv[1]
    else:
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        json_path = filedialog.askopenfilename(title="Select save file", filetypes=[("Save Files", "*.save")])
        root.destroy()
    if not json_path:
        print("No file selected.")
        return
    window("Sandustry Save Visualizer", Map(json_path)).render()


if __name__ == "__main__":
    main()
