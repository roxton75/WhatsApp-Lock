# 🔐 WhatsApp Desktop Lock

A clean and seamless **overlay lock screen** for WhatsApp Desktop, built using **Python + CustomTkinter**.  
Protects your chats whenever WhatsApp is opened in the foreground.

---

## ✨ Features

- **Blur Overlay Lock Screen** — prevents interaction until password is entered  
- **WhatsApp UI Themed Design** — visually fits the native app  
- **Password Visibility Toggle** — subtle, smooth transitions  
- **Foreground Detection** — lock triggers only when WhatsApp is active  
- **Auto-Unlock Session** — stays unlocked until WhatsApp is closed  
- **Lightweight** — almost no CPU usage
- **Optional Auto-Start at Login** — runs silently in background  

---

## 🖥️ Preview
Demo: [Live Preview](https://www.linkedin.com/posts/rudrx75_just-finished-building-a-small-utility-for-activity-7393051089551650816-fVce)
<img width="1215" height="706" alt="image" src="https://github.com/user-attachments/assets/b4d109a7-d949-4ffc-be58-fcf45d3e079b" />

---

## 🧠 How It Works

1. Script runs in the background.
2. Detects when **WhatsApp Desktop** becomes the active window.
3. Displays a **blurred overlay lock** requiring password entry.
4. Once correct password is entered:
   - Overlay disappears
   - WhatsApp is usable normally until closed.

---

## 📦 Installation

### 1) Clone Repository
```bash
git clone https://github.com/roxton75/whatsapp-lock.git
cd whatsapp-lock
````

### 2) Install Dependencies

```bash
pip install customtkinter pillow psutil pygetwindow
```

### 3) Set Password

Create a file named `pass.txt` :

```
your_password
```

Write **one line only** containing your password.

---

## ▶️ Run

```bash
python main.py
```

---

## 🚀 Optional: Auto-Start on Windows Login

1. Build executable:

   ```bash
   pyinstaller --noconsole --onefile --add-data "ui/assets;ui/assets" --add-data "pass.txt;." main.py
   ```

2. Place shortcut of the generated `.exe` in (Startup Folder):

   ```
   Win + R → shell:startup     
   ```
   
3. If the above method doesn't work then try:

   🔄 Enable Auto-Start (Recommended)

   To make WhatsApp Lock launch automatically when you log in to Windows, set it up using Task Scheduler.
  
     1) Open Task Scheduler
      ```
         Win + R → taskschd.msc → Enter
      ```
     2) Create a New Task
         
        - Click Action → Create Task
        - Name it: `WhatsApp Lock`
        - Enable:
            ✅ Run only when user is logged on
            ✅ Run with highest privileges
     3) Add Trigger
      
        - Go to the Triggers tab → New
        - Begin the task: At log on
        - User: Select your account
        - Click OK
      
     4) Add Action
      
        - Go to the Actions tab → New
        - Action: Start a program
        - Program/script: Select your .bat launcher file
        - Click OK
  
     5) Adjust Conditions (Important for Laptops)
      
        - Go to the Conditions tab
        - Uncheck:
          Start only if the computer is on AC power
      
     6) Save
      
        - Click OK
        - Close Task Scheduler
  
    ✅ Now WhatsApp Lock will automatically run silently every time you log in.

---

## 📂 Project Structure

```
whatsapp-lock/
│ main.py
│ pass.txt
│ README.md
│
├─ core/
│   └─ overlay.py
│
├─ ui/
│   ├─ lock_ui.py
│   └─ assets/
│       ├─ logo48.png
│       ├─ eye-active.png
│       ├─ eye-inactive.png
│       └─ ...
```

---

## ⚠️ Security Note

This project does **not** modify WhatsApp, hook memory, or intercept messages.
It simply blocks user access visually at the UI level.

---



Made with EFFORTS !!
by **[@roxton75](https://github.com/roxton75)**

⭐ If this project helped you, star the repository — it motivates future upgrades.



