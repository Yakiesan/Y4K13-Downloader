import customtkinter as ctk
from yt_dlp import YoutubeDL
import threading
import os
import sys
from PIL import Image

# Essential for the EXE to find Miku inside itself
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class Y4K13_Downloader(ctk.CTk):
    def __init__(self):
        super().__init__()

        # YTMP3 Inspired Theme
        self.title("Y4K13 - PRO DOWNLOADER")
        self.geometry("700x500")
        self.configure(fg_color="#121212")

        # Title Section
        self.label = ctk.CTkLabel(self, text="Y4K13", font=("Arial Black", 55), text_color="#00D084")
        self.label.pack(pady=(50, 5))
        
        self.sub = ctk.CTkLabel(self, text="High-Speed Secure Extraction", font=("Consolas", 14), text_color="#777777")
        self.sub.pack(pady=(0, 30))

        # URL Input
        self.url_var = ctk.StringVar()
        self.entry = ctk.CTkEntry(self, placeholder_text="Paste your link here...", width=520, height=50, 
                                  border_color="#00D084", fg_color="#1e1e1e", textvariable=self.url_var)
        self.entry.pack(pady=10)

        # Mode Selection
        self.mode = ctk.StringVar(value="MP3")
        self.mode_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.mode_frame.pack(pady=10)

        self.rb_mp3 = ctk.CTkRadioButton(self.mode_frame, text="MP3", variable=self.mode, value="MP3", text_color="white", fg_color="#00D084", hover_color="#00b070")
        self.rb_mp3.grid(row=0, column=0, padx=20)
        self.rb_mp4 = ctk.CTkRadioButton(self.mode_frame, text="MP4", variable=self.mode, value="MP4", text_color="white", fg_color="#00D084", hover_color="#00b070")
        self.rb_mp4.grid(row=0, column=1, padx=20)

        # The Big Button
        self.btn = ctk.CTkButton(self, text="CONVERT", width=180, height=50, corner_radius=8,
                                 fg_color="#00D084", text_color="black", font=("Arial", 18, "bold"),
                                 command=self.start_process)
        self.btn.pack(pady=20)

        self.status = ctk.CTkLabel(self, text="READY", text_color="#00D084", font=("Consolas", 12))
        self.status.pack()

        # --- MIKU PEAKING LOGIC ---
        miku_img_path = resource_path("miku_peak.png")
        if os.path.exists(miku_img_path):
            img = Image.open(miku_img_path)
            self.miku_ctk = ctk.CTkImage(light_image=img, dark_image=img, size=(250, 180))
            self.miku_label = ctk.CTkLabel(self, image=self.miku_ctk, text="")
            self.miku_label.place(relx=0.0, rely=1.0, anchor="sw")

    def start_process(self):
        self.btn.configure(state="disabled")
        threading.Thread(target=self.download, daemon=True).start()

    def download(self):
        url = self.url_var.get()
        if not url:
            self.status.configure(text="❌ LINK MISSING", text_color="red")
            self.btn.configure(state="normal")
            return

        self.status.configure(text="🛰️ BYPASSING SECURITY...", text_color="yellow")
        
        # PRO ANTI-BOT SETTINGS
        ydl_opts = {
            'format': 'bestaudio/best' if self.mode.get() == "MP3" else 'best',
            'impersonate': 'chrome', # Mimics real browser TLS/JA3 fingerprint
            'nocheckcertificate': True,
            'quiet': True,
            'no_warnings': True,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }

        if self.mode.get() == "MP3":
            ydl_opts['postprocessors'] = [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '192'}]

        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            self.status.configure(text="✅ DONE: CHECK FOLDER", text_color="#00D084")
        except Exception:
            self.status.configure(text="❌ BLOCKED OR INVALID LINK", text_color="red")
        
        self.btn.configure(state="normal")

if __name__ == "__main__":
    app = Y4K13_Downloader()
    app.mainloop()