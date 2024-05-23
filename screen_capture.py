import tkinter as tk
import mss
from PIL import Image

class ScreenCapture:
    def __init__(self):
        self.screenshot_path = None
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the main window

    def capture_region(self):
        """Captures a region of the screen selected by the user."""

        # Get the monitor with the mouse pointer
        with mss.mss() as sct:
            monitor = sct.monitors[1]  # Monitor 1 is usually the primary monitor

        # Create a transparent window for selection
        select_window = tk.Toplevel(self.root)
        select_window.attributes("-alpha", 0.5)
        select_window.attributes("-fullscreen", True)
        select_window.overrideredirect(True)

        canvas = tk.Canvas(select_window, bg="white", cursor="cross")
        canvas.pack(fill=tk.BOTH, expand=True)

        start_x, start_y = 0, 0
        rect = None

        def on_button_press(event):
            nonlocal start_x, start_y, rect
            start_x, start_y = event.x, event.y
            rect = canvas.create_rectangle(start_x, start_y, start_x, start_y, outline="red")

        def on_button_motion(event):
            nonlocal rect
            canvas.coords(rect, start_x, start_y, event.x, event.y)

        def on_button_release(event):
            nonlocal monitor
            global screenshot_path
            select_window.destroy()
            self.root.quit()

            x1, y1 = min(start_x, event.x), min(start_y, event.y)
            x2, y2 = max(start_x, event.x), max(start_y, event.y)

            # Adjust the coordinates to the specific monitor
            monitor["left"] += x1
            monitor["top"] += y1
            monitor["width"] = x2 - x1
            monitor["height"] = y2 - y1

            # Capture the selected area on the correct monitor
            with mss.mss() as sct:
                screenshot = sct.grab(monitor)
                image = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
                screenshot_path = "screenshot.png"
                image.save(screenshot_path)  # Save the screenshot to a file

        canvas.bind("<ButtonPress-1>", on_button_press)
        canvas.bind("<B1-Motion>", on_button_motion)
        canvas.bind("<ButtonRelease-1>", on_button_release)

        self.root.mainloop()
        return screenshot_path

# Create an instance of the class to use in interface.py
screen_capture_instance = ScreenCapture()


