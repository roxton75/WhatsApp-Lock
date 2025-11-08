import time
import psutil
import customtkinter as ctk
from core.overlay import Overlay

import pygetwindow as gw

def is_whatsapp_active():
    try:
        win = gw.getActiveWindow()
        return win and "whatsapp" in win.title.lower()
    except:
        return False

def is_whatsapp_running():
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] and proc.info['name'].lower() == "whatsapp.exe":
            return True
    return False

def main():
    time.sleep(3) # Wait for Windows & WhatsApp to settle after boot
    locked = False

    while True:
        if is_whatsapp_running() and is_whatsapp_active() and not locked:
            locked = True
            root = ctk.CTk()
            Overlay(root)
            root.mainloop()

            # If user unlocked, wait until WhatsApp closes before relocking again
            if getattr(root, "unlocked", False):
                while is_whatsapp_running():
                    time.sleep(0.5)
                locked = False
            else:
                # Overlay closed without unlock (rare); allow relock logic
                locked = False

        elif not is_whatsapp_running():
            locked = False

        time.sleep(0.5)

if __name__ == "__main__":
    main()
