import tkinter as tk
import ctypes
import threading
import ctypes.wintypes

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
import sys
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

import time

# Initialize the initial mouse state
initial_mouse_state = None

def check_mouse_state():
    global initial_mouse_state
    
    # Add a delay to avoid checking the initial state too quickly
    time.sleep(0.1)
    
    # Get the initial mouse state after the delay
    initial_mouse_state = ctypes.windll.user32.GetAsyncKeyState(0x01)
    print(initial_mouse_state)
    isActive = True
    while True:
        # Check the current state of the left mouse button
        current_mouse_state = ctypes.windll.user32.GetAsyncKeyState(0x01)

        # Compare the current state to the initial state
        if current_mouse_state != initial_mouse_state:
            print(current_mouse_state)
            # The mouse state has changed, trigger your function here
            if current_mouse_state  == 32769 or current_mouse_state == 0 and isActive:
                # Mouse button pressed
                print("Mouse button pressed or released")
                isActive = False
                copy_file()
                paste()
                app.quit()
                # Call your function when the button is pressed
            
            # Update the initial state
            initial_mouse_state = current_mouse_state


def start_mouse_check_thread():
    mouse_check_thread = threading.Thread(target=check_mouse_state)
    mouse_check_thread.daemon = True
    mouse_check_thread.start()


def copy_file():
    import subprocess
    cmd = "Get-Item -LiteralPath \"{}\" | Set-Clipboard".format(file_path)
    # print(cmd)
    subprocess.run(["powershell", "-command", cmd], shell=True)


def paste():
    import pyautogui
    # import pygetwindow as gw

    # Get the active window
    pyautogui.leftClick()
    # active_window = gw.getActiveWindow()
    pyautogui.hotkey('ctrl', 'v')  # Use 'command' on macOS
    app.quit()  # Quit the application when the mouse button is released

    # # if active_window:
    # if active_window:
    #     print(active_window)
    #     active_window.activate()
    # else:
    #     print("No active window found.")

def handle_key_event(event):
    print("EXIT")
    app.quit()  # Quit the application when a key is pressed

update_position()
app.bind_all("<Escape>", handle_key_event)  # Bind all key presses to the handle_key_event function
start_mouse_check_thread()
app.mainloop()
