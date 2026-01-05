import customtkinter as ctk
from yt_dlp import YoutubeDL
import threading
import multiprocessing
import sys
import os

class Y4K13_Downloader(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Branding
        self.title("Y4K13 Downloader")
        self.geometry("700x520")
        self.configure(fg_color="#0a0a0a")
        self.resizable(False, False)

        # 1. Neon Header with Animation-ready Font
        self.header = ctk.CTkLabel(self, text="Y4K13", font=("Arial Black", 75), text_color="#00D084")
        self.header.pack(pady=(40, 5))
        
        self.tagline = ctk.CTkLabel(self, text="ULTIMATE MEDIA EXTRACTOR", font=("Consolas", 11), text_color="#444444")
        self.tagline.pack(pady=(0, 20))

        # 2. Glowing URL Input
        self.url_var = ctk.StringVar()
        self.entry = ctk.CTkEntry(self, placeholder_text="Paste your link (YouTube, TikTok, FB, etc.)...", 
                                  width=520, height=52, border_color="#00D084", 
                                  fg_color="#121212", textvariable=self.url_var,
                                  font=("Arial", 14))
        self.entry.pack(pady=10)

        # 3. Format Selection
        self.mode = ctk.StringVar(value="MP4")
        self.radio_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.radio_frame.pack(pady=10)
        
        ctk.CTkRadioButton(self.radio_frame, text="VIDEO (MP4)", variable=self.mode, value="MP4", text_color="white", fg_color="#00D084", border_color="#00D084").grid(row=0, column=0, padx=20)
        ctk.CTkRadioButton(self.radio_frame, text="AUDIO (MP3)", variable=self.mode, value="MP3", text_color="white", fg_color="#00D084", border_color="#00D084").grid(row=0, column=1, padx=20)

        # 4. Animated Progress Section
        self.prog_label = ctk.CTkLabel(self, text="READY", font=("Arial Black", 15), text_color="#555555")
        self.prog_label.pack(pady=(25, 5))
        
        self.bar = ctk.CTkProgressBar(self, width=500, height=14, progress_color="#00D084", fg_color="#1a1a1a")
        self.bar.set(0)
        self.bar.pack(pady=5)

        # 5. The "Convert" Action
        self.dl_btn = ctk.CTkButton(self, text="START CONVERSION", width=260, height=58, 
                                    fg_color="#00D084", text_color="black", font=("Arial Black", 18),
                                    hover_color="#00ff9d", command=self.trigger)
        self.dl_btn.pack(pady=25)

    def progress_hook(self, d):
        """Updates the bar and percentage from 1% to 100%"""
        if d['status'] == 'downloading':
            p = d.get('_percent_str', '0%').replace('%','').strip()
            try:
                percent_val = float(p)
                self.bar.set(percent_val / 100)
                self.prog_label.configure(text=f"PROGRESS: {int(percent_val)}%", text_color="#00D084")
            except: pass
        elif d['status'] == 'finished':
            self.bar.set(1.0)
            self.prog_label.configure(text="CONVERSION COMPLETE!", text_color="#00D084")

    def trigger(self):
        url = self.url_var.get().strip()
        if not url: return
        self.dl_btn.configure(state="disabled", text="PROCESSING...")
        self.prog_label.configure(text="BYPASSING BOT PROTECTION...", text_color="#00D084")
        threading.Thread(target=self.engine, args=(url,), daemon=True).start()

    def engine(self, url):
        is_mp3 = self.mode.get() == "MP3"
        ydl_opts = {
            'format': 'bestaudio/best' if is_mp3 else 'best',
            'progress_hooks': [self.progress_hook],
            'impersonate': 'chrome', # Pro anti-bot bypass
            'nocheckcertificate': True,
            'quiet': True,
        }
        if is_mp3:
            ydl_opts['postprocessors'] = [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '192'}]

        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        except Exception:
            self.prog_label.configure(text="ERROR: ACCESS BLOCKED", text_color="#FF4B4B")
        
        self.dl_btn.configure(state="normal", text="START CONVERSION")

if __name__ == "__main__":
    multiprocessing.freeze_support()
    app = Y4K13_Downloader()
    app.mainloop()