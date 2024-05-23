import tkinter as tk
from tkinter import ttk
import pyperclip
import webbrowser
import keyboard
from screen_capture import screen_capture_instance
from qr_decode import decode_qr_code

# --- Function to handle decoded data ---
def handle_decoded_data(decoded_data):
    if decoded_data.startswith(("http://", "https://")):
        webbrowser.open(decoded_data)
    elif decoded_data.endswith((".jpg", ".jpeg", ".png", ".gif")):
        webbrowser.open(decoded_data)
    elif decoded_data.endswith((".mp4", ".avi", ".mov")):
        webbrowser.open(decoded_data)
    else:
        pyperclip.copy(decoded_data)
        status_label.config(text="Copied to clipboard: " + decoded_data)

# --- Function to scan QR code ---
def scan_qr_code():
    screenshot_path = screen_capture_instance.capture_region()

    if not screenshot_path:
        status_label.config(text="No screenshot captured.")
        return

    decoded_data = decode_qr_code(screenshot_path)

    if decoded_data:
        handle_decoded_data(decoded_data)
        status_label.config(text="QR code scanned successfully!")
    else:
        status_label.config(text="No QR code found")

# --- Function to schedule QR code scan in the main thread ---
def schedule_scan_qr_code():
    window.after(0, scan_qr_code)

# --- Create the main window ---
window = tk.Tk()
window.title("Screen QR Code Reader")
window.configure(bg="#f0f0f0")

# --- Styling ---
style = ttk.Style()
style.theme_use("clam")
style.configure("TLabel", background="#f0f0f0", foreground="#333")

# --- Create and place widgets ---
title_label = ttk.Label(window, text="Screen QR Code Reader", font=("Arial", 16))
title_label.pack(pady=20)

instructions_label = ttk.Label(window, text="Press Ctrl+Alt+Q to start scanning")
instructions_label.pack()

status_label = ttk.Label(window, text="", font=("Arial", 12))
status_label.pack(pady=10)

# --- Register the keyboard shortcut ---
keyboard.add_hotkey("ctrl+alt+q", schedule_scan_qr_code)

# --- Run the GUI ---
window.mainloop()


