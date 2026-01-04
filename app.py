import customtkinter as ctk
from yt_dlp import YoutubeDL
import threading
import os
import sys
import tkinter as tk # Use built-in tkinter for the image

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class Y4K13_Lite(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Y4K13 ULTIMATE")
        self.geometry("700x500")
        self.configure(fg_color="#0a0a0a")

        # UI Header
        self.logo = ctk.CTkLabel(self, text="Y4K13", font=("Impact", 60), text_color="#00FF41")
        self.logo.pack(pady=(40, 5))
        
        # URL Input
        self.url_var = ctk.StringVar()
        self.entry = ctk.CTkEntry(self, placeholder_text="PASTE LINK...", width=500, height=50, 
                                  border_color="#00FF41", fg_color="#111111", textvariable=self.url_var)
        self.entry.pack(pady=10)

        # Download Button
        self.dl_btn = ctk.CTkButton(self, text="DOWNLOAD", width=220, height=55, 
                                    fg_color="#00FF41", text_color="black", font=("Impact", 20),
                                    command=self.start_thread)
        self.dl_btn.pack(pady=20)

        self.status = ctk.CTkLabel(self, text="READY", text_color="#00FF41")
        self.status.pack()

        # --- MIKU IMAGE (WITHOUT PIL) ---
        miku_file = resource_path("miku_peak.png")
        if os.path.exists(miku_file):
            # PhotoImage is built into Python/Tkinter - No PIL needed!
            self.miku_img = tk.PhotoImage(file=miku_file)
            
            # Since PhotoImage can't resize easily, we display it in a standard Label
            self.miku_label = tk.Label(self, image=self.miku_img, bg="#0a0a0a", borderwidth=0)
            self.miku_label.place(relx=1.0, rely=1.0, anchor="se")

    def start_thread(self):
        threading.Thread(target=self.run_download, daemon=True).start()

    def run_download(self):
        url = self.url_var.get()
        if not url: return
        self.status.configure(text="🛰️ BYPASSING...", text_color="yellow")
        
        ydl_opts = {
            'format': 'best',
            'impersonate': 'chrome',
            'nocheckcertificate': True,
            'quiet': True,
        }

        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            self.status.configure(text="✅ DONE", text_color="#00FF41")
        except:
            self.status.configure(text="❌ FAILED", text_color="red")

if __name__ == "__main__":
    app = Y4K13_Lite()
    app.mainloop()