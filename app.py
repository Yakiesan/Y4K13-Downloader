import customtkinter as ctk
from yt_dlp import YoutubeDL
import threading
import sys
import os
import multiprocessing
from fake_useragent import UserAgent

class Y4K13_Ultimate(ctk.CTk):
    def __init__(self):
        super().__init__()

        # UI Setup
        self.title("Y4K13 Ultimate Downloader")
        self.geometry("700x450")
        self.configure(fg_color="#0a0a0a")
        self.resizable(False, False)

        # Labels
        self.header = ctk.CTkLabel(self, text="Y4K13", font=("Arial Black", 65), text_color="#00D084")
        self.header.pack(pady=(40, 5))
        
        self.sub = ctk.CTkLabel(self, text="UNIVERSAL WEB EXTRACTOR (TIKTOK/FB/IG/YT)", 
                                font=("Consolas", 12), text_color="#555555")
        self.sub.pack(pady=(0, 30))

        # URL Input
        self.url_var = ctk.StringVar()
        self.entry = ctk.CTkEntry(self, placeholder_text="Paste Link (TikTok, FB, IG, etc.)...", 
                                  width=550, height=50, border_color="#00D084", 
                                  fg_color="#121212", textvariable=self.url_var)
        self.entry.pack(pady=10)

        # Format Toggles
        self.mode = ctk.StringVar(value="MP4")
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.pack(pady=10)
        
        ctk.CTkRadioButton(self.btn_frame, text="VIDEO (MP4)", variable=self.mode, value="MP4", text_color="white", fg_color="#00D084").grid(row=0, column=0, padx=20)
        ctk.CTkRadioButton(self.btn_frame, text="AUDIO (MP3)", variable=self.mode, value="MP3", text_color="white", fg_color="#00D084").grid(row=0, column=1, padx=20)

        # Process Button
        self.dl_btn = ctk.CTkButton(self, text="CONVERT & DOWNLOAD", width=250, height=55, 
                                    fg_color="#00D084", text_color="black", font=("Arial Black", 16),
                                    command=self.start_engine)
        self.dl_btn.pack(pady=20)

        self.status = ctk.CTkLabel(self, text="STATUS: IDLE", text_color="#444444")
        self.status.pack()

    def start_engine(self):
        url = self.url_var.get().strip()
        if not url: return
        self.dl_btn.configure(state="disabled", text="PROCESSING...")
        threading.Thread(target=self.run_download, args=(url,), daemon=True).start()

    def run_download(self, url):
        self.update_status("🛰️ INJECTING BROWSER FINGERPRINT...", "#00D084")
        
        ua = UserAgent()
        is_mp3 = self.mode.get() == "MP3"
        
        # PRO-LEVEL ANTI-BOT SETTINGS
        ydl_opts = {
            'format': 'bestaudio/best' if is_mp3 else 'bestvideo+bestaudio/best',
            'impersonate': 'chrome',      # Uses curl-cffi to mimic Chrome 120+
            'http_headers': {
                'User-Agent': ua.random,   # Rotates identity to avoid IP bans
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-us,en;q=0.5',
            },
            'nocheckcertificate': True,
            'quiet': True,
            'no_warnings': True,
            'noplaylist': True,
            'extract_flat': False,
        }

        if is_mp3:
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]

        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            self.update_status("✅ DOWNLOAD COMPLETE", "#00D084")
        except Exception as e:
            self.update_status("❌ ACCESS DENIED OR BOT DETECTED", "red")
        
        self.dl_btn.configure(state="normal", text="CONVERT & DOWNLOAD")

    def update_status(self, text, color):
        self.status.configure(text=text, text_color=color)

if __name__ == "__main__":
    multiprocessing.freeze_support()
    app = Y4K13_Ultimate()
    app.mainloop()