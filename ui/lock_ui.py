import customtkinter as ctk
from customtkinter import CTkImage
from PIL import Image, ImageFilter, ImageGrab, ImageTk
import psutil
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class LockUI(ctk.CTkFrame):

        def __init__(self, master, on_unlock):
            super().__init__(master)
            self.configure(fg_color="transparent")
            self.on_unlock = on_unlock

            # Shadow frame (behind popup)
            self.shadow = ctk.CTkFrame(
                master,
                fg_color="#1A1A1A",     # shadow color (black)
                corner_radius=12
            )
            self.shadow.configure(width=500, height=200)
            self.shadow.place(relx=0.5, rely=0.5, anchor="center", x=1.5, y=1.5)  # slight offset


            # Create the popup ONCE, as a child of self
            self.popup = ctk.CTkFrame(
                master,
                fg_color="#222222",
                corner_radius=10,
                border_width=2,
                border_color="#333333"
            )

            #  Set size BEFORE children so grid doesn’t shrink it
            self.popup.configure(width=500, height=200)
            self.popup.grid_propagate(False)  # <--- IMPORTANT FIX

            self.popup.place(relx=0.5, rely=0.5, anchor="center")

            # Now apply column config AFTER propagate False
            self.popup.columnconfigure(0, minsize=36)
            self.popup.columnconfigure(1, weight=1, minsize=180)
            self.popup.columnconfigure(2, minsize=44)


            # WhatsApp logo at top left
            # logo_path = os.path.join(os.path.dirname(__file__), "assets", "logo48.png")
            logo_path = resource_path("ui/assets/logo48.png")
            logo_img = Image.open(logo_path).resize((28, 28), Image.LANCZOS)
            self.logo_photo = CTkImage(light_image=logo_img, dark_image=logo_img, size=(28, 28))
            self.logo_label = ctk.CTkLabel(self.popup, image=self.logo_photo, text="", width=36)
            self.logo_label.grid(row=0, column=0, padx=(18, 4), pady=(18, 0), sticky="w")

            # Title (immediately right of logo)
            self.title = ctk.CTkLabel(
                self.popup,
                text="WhatsApp Lock",
                font=("Netflix Sans", 15, "bold"),
                text_color="white",
                anchor="w"
            )
            self.title.grid(row=0, column=1, columnspan=2, sticky="w", padx=(0, 0), pady=(18, 0))

            # Password field and eye icon in a row
            self.password_var = ctk.StringVar()
            # Password field frame for proportional layout
            self.password_frame = ctk.CTkFrame(self.popup, fg_color="transparent")
            self.password_frame.grid(row=1, column=0, columnspan=3, padx=(18, 18), pady=(24, 0), sticky="ew")
            self.password_frame.columnconfigure(0, weight=1)
            self.password_frame.columnconfigure(1, minsize=40)

          
            self.password_entry = ctk.CTkEntry(
                self.password_frame,
                textvariable=self.password_var,
                show="",   # Start unmasked so placeholder is visible
                width=1,
                height=36,
                font=("Netflix Sans", 13),
                border_color="#3a3a3a",
                fg_color="#2C2C2C",
                text_color="#ffffff",
                placeholder_text="Enter Password",
                placeholder_text_color="#555555"
            )
            
            def on_pw_hover(e):
                self.password_entry.configure(border_color="#474747")

            def on_pw_leave(e):
                self.password_entry.configure(border_color="#3a3a3a")

            self.password_entry.bind("<Enter>", on_pw_hover)
            self.password_entry.bind("<Leave>", on_pw_leave)

            
            self.password_entry.bind("<Return>", lambda event: self.check_password())

            self.password_entry.bind("<KeyRelease>", lambda e: self.password_entry.configure(show="•") if self.password_var.get() != "" and not self.show_password else self.password_entry.configure(show=""))

            self.password_entry.configure(width=260)
            self.password_entry.grid(row=0, column=0, sticky="ew", padx=(11, 0))
            
            # Track password visibility
            self.show_password = False
            

            # Eye PNG icon setup (CTkImage)
            eye_inactive_path = resource_path("ui/assets/eye-inactive.png")
            eye_active_path = resource_path("ui/assets/eye-active.png")
            eye_inactive_img = Image.open(eye_inactive_path).resize((24, 24), Image.LANCZOS)
            eye_active_img = Image.open(eye_active_path).resize((24, 24), Image.LANCZOS)
            self.eye_icon_inactive = CTkImage(light_image=eye_inactive_img, dark_image=eye_inactive_img, size=(24, 24))
            self.eye_icon_active = CTkImage(light_image=eye_active_img, dark_image=eye_active_img, size=(24, 24))
            self.eye_btn = ctk.CTkButton(
                self.password_frame,
                text="",
                image=self.eye_icon_inactive,
                width=36,
                height=36,
                command=self.toggle_password,
                fg_color="transparent",
                hover_color="#252525",
                corner_radius=5
            )
            self.eye_btn.grid(row=0, column=1, sticky="e")

            # Button frame for bottom right
            self.button_frame = ctk.CTkFrame(self.popup, fg_color="transparent")
            self.button_frame.grid(row=2, column=2, padx=(0, 32), pady=(32, 18), sticky="se")

            self.exit_btn = ctk.CTkButton(
                self.button_frame,
                text="Exit",
                width=90,
                height=36,
                command=self.on_exit,
                fg_color="transparent",
                hover_color="#353535",
                text_color="#ffffff",
                font=("Netflix Sans", 14, "bold"),
                border_width=2,
                border_color="#353535",
                corner_radius=7,
                border_spacing=0
            )
            self.exit_btn.pack(side="left", padx=(0, 10))

            self.enter_btn = ctk.CTkButton(
                self.button_frame,
                text="Enter",
                width=90,
                height=36,
                command=self.check_password,
                fg_color="#06b147",  # WhatsApp green
                hover_color="#12e25f",
                text_color="#1d1d1d",
                font=("Netflix Sans", 14, "bold"),
                border_width=2,
                border_color="#353535",
                corner_radius=7,
                border_spacing=0
            )
            self.enter_btn.pack(side="left")

            # Gains Focus on password entry
            self.master.after(100, lambda: self.password_entry.focus_force())
            self.password_entry.bind("<FocusOut>", lambda e: self.password_entry.focus_force())
            

        # No overlay redraw needed  
        def toggle_password(self):
            self.show_password = not self.show_password
            if self.show_password:
                self.password_entry.configure(show="")
                self.eye_btn.configure(image=self.eye_icon_active)
            else:
                self.password_entry.configure(show="•")
                self.eye_btn.configure(image=self.eye_icon_inactive)
        
        # With .txt file
        def check_password(self):
            # Load password from password.txt
            try:
                PASSWORD_FILE = resource_path("pass.txt")
                with open(PASSWORD_FILE, "r") as f:
                    saved_password = f.read().strip()
            except:
                saved_password = "raju"  # fallback if file missing
                print("Warning: password.txt not found, using fallback password.")

            entered = self.password_var.get().strip()

            if entered == saved_password:
                self.on_unlock()
                print("Unlocked")
            else:
                # Shake effect for incorrect password
                def shake(offset=0):
                    if offset < 6:
                        self.popup.place(x=2 if offset % 2 == 0 else -2, relx=0.5, rely=0.5, anchor="center")
                        self.password_entry.configure(border_color="#E46060")
                        self.after(30, lambda: shake(offset + 1))
                    else:
                        self.popup.place(x=0, relx=0.5, rely=0.5, anchor="center")
                        self.password_entry.configure(border_color="#3a3a3a")
                shake()

        
        
        def on_exit(self):
            # Kill WhatsApp, then close overlay cleanly
            try:
                for p in psutil.process_iter(['name']):
                    if p.info['name'] and p.info['name'].lower() == "whatsapp.exe":
                        p.terminate()
            except Exception:
                pass
            self.on_unlock()   # close overlay
