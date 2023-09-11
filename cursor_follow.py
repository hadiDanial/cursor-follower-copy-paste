import tkinter as tk
import ctypes
import threading
import ctypes.wintypes
import sys
import pygetwindow as gw
import pyautogui
import subprocess

# Built to .exe with the following command:
# pyinstaller --onefile --noconsole p:/path/to/script/cursor_follow.py 
# need to install modules with pip: pyinstaller, pygetwindow, pyautogui

app = tk.Tk()
app.title("")  # Set an empty string for the title to hide it
app.geometry("64x64")  # Set the window size

# Hide the title bar and borders
app.overrideredirect(True)
# app.configure(bg="#FF0000")  # Replace "#FF0000" with your desired color in hexadecimal format
app.wm_attributes("-topmost", 1)
image_path = "dragIcon.png"  # Replace with the path to your image
background_image = tk.PhotoImage(file=image_path)

# Create a label to display the transparent background image
background_label = tk.Label(app, image=background_image)
background_label.place(relwidth=1, relheight=1)
# Global variable to track mouse button state
mouse_button_pressed = False
file_path = ""
if len(sys.argv) > 1:
    file_path = sys.argv[1]  # The first argument (index 0) is the script name
else:
    app.quit()


def update_position():
    cursor_position = ctypes.wintypes.POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(cursor_position))
    x, y = cursor_position.x, cursor_position.y
    app.geometry(f"+{x+2}+{y+2}")  # Move the app to the cursor's position
    app.after(10, update_position)

def check_mouse_state():
    global mouse_button_pressed
    while True:
        # Check if the left mouse button is pressed
        if ctypes.windll.user32.GetAsyncKeyState(0x01) != 0:
            mouse_button_pressed = True
        else:
            if mouse_button_pressed:
                copy_file()
                paste()
                app.quit()  # Quit the application when the mouse button is released
            mouse_button_pressed = False

def start_mouse_check_thread():
    mouse_check_thread = threading.Thread(target=check_mouse_state)
    mouse_check_thread.daemon = True
    mouse_check_thread.start()


def copy_file():
    cmd = "Get-Item -LiteralPath \"{}\" | Set-Clipboard".format(file_path)
    print(cmd)
    subprocess.run(["powershell", "-command", cmd], shell=True)


def paste():
    # Get the active window
    active_window = gw.getActiveWindow()
    # if active_window:
    if active_window:
        print(active_window)
        active_window.activate()
        pyautogui.hotkey('ctrl', 'v')  # Use 'command' on macOS
    else:
        print("No active window found.")

def handle_key_event(event):
    app.quit()  # Quit the application when a key is pressed

update_position()
start_mouse_check_thread()
app.bind_all("<Key>", handle_key_event)  # Bind all key presses to the handle_key_event functiondecrypted.pdf
app.mainloop()
