import customtkinter as ctk
from customtkinter import CTkImage
from PIL import ImageGrab, ImageFilter
from ui.lock_ui import LockUI
import win32gui, win32con, win32api, time


class Overlay:
    def __init__(self, root):
        self.root = root
        self.root.unlocked = False
        self.blur_after_id = None

        self.root.attributes("-topmost", True)
        self.root.state("zoomed")
        self.root.overrideredirect(True)
        
        self.root.update_idletasks()
        hwnd = win32gui.GetForegroundWindow()

        # Force overlay to the real foreground window
        def enforce_focus():
            try:
                win32gui.SetForegroundWindow(hwnd)
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                self.root.focus_force()
                self.root.lift()
                self.root.grab_set()
            except:
                pass

        # Call a few times to override WhatsApp auto-focus
        for delay in (0, 50, 120, 250):
            self.root.after(delay, enforce_focus)

        screenshot = ImageGrab.grab()
        blurred = screenshot.filter(ImageFilter.GaussianBlur(4))

        self.bg_img = CTkImage(light_image=blurred, size=(blurred.width, blurred.height))
        self.bg_label = ctk.CTkLabel(self.root, image=self.bg_img, text="")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.lock_ui = LockUI(self.root, self.on_unlock)   # <-- keep a ref

        self.update_blur()

    def update_blur(self):
        try:
            screenshot = ImageGrab.grab()
            blurred = screenshot.filter(ImageFilter.GaussianBlur(5))
            self.bg_img = CTkImage(light_image=blurred, size=(blurred.width, blurred.height))
            self.bg_label.configure(image=self.bg_img)
            self.blur_after_id = self.bg_label.after(120, self.update_blur)
        except Exception:
            # Guard against callbacks after destroy
            pass

    def on_unlock(self):
        # mark unlocked, stop timers, then close
        self.root.unlocked = True                      # <-- add
        if self.blur_after_id:
            try:
                self.bg_label.after_cancel(self.blur_after_id)
            except Exception:
                pass
        self.root.destroy()