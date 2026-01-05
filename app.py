import customtkinter as ctk
from yt_dlp import YoutubeDL
import threading
import os
import sys
import multiprocessing

class Y4K13_Ultimate(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Config
        self.title("Y4K13 Ultimate")
        self.geometry("700x520")
        self.configure(fg_color="#0a0a0a")
        self.resizable(False, False)

        # 1. Animated Header (Pulsing Effect)
        self.header = ctk.CTkLabel(self, text="Y4K13", font=("Arial Black", 70), text_color="#00D084")
        self.header.pack(pady=(40, 5))
        
        self.sub = ctk.CTkLabel(self, text="UNIVERSAL EXTRACTION ENGINE", font=("Consolas", 12), text_color="#555555")
        self.sub.pack(pady=(0, 20))

        # 2. URL Input with Glow Border
        self.url_var = ctk.StringVar()
        self.entry = ctk.CTkEntry(self, placeholder_text="Paste Link Here...", 
                                  width=550, height=50, border_color="#00D084", 
                                  fg_color="#121212", textvariable=self.url_var)
        self.entry.pack(pady=10)

        # 3. Mode Selection
        self.mode = ctk.StringVar(value="MP4")
        self.radio_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.radio_frame.pack(pady=10)
        
        ctk.CTkRadioButton(self.radio_frame, text="VIDEO (MP4)", variable=self.mode, value="MP4", text_color="white", fg_color="#00D084").grid(row=0, column=0, padx=20)
        ctk.CTkRadioButton(self.radio_frame, text="AUDIO (MP3)", variable=self.mode, value="MP3", text_color="white", fg_color="#00D084").grid(row=0, column=1, padx=20)

        # 4. Progress Tracking Section
        self.progress_label = ctk.CTkLabel(self, text="0%", font=("Arial Black", 14), text_color="#00D084")
        self.progress_label.pack(pady=(20, 0))
        
        self.progress_bar = ctk.CTkProgressBar(self, width=500, height=12, progress_color="#00D084", fg_color="#1a1a1a")
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=10)

        # 5. Convert Button
        self.dl_btn = ctk.CTkButton(self, text="INITIALIZE DOWNLOAD", width=250, height=55, 
                                    fg_color="#00D084", text_color="black", font=("Arial Black", 16),
                                    hover_color="#00ff9d", command=self.start_engine)
        self.dl_btn.pack(pady=20)

        self.status = ctk.CTkLabel(self, text="SYSTEM READY", text_color="#444444")
        self.status.pack()

    def update_status(self, text, color):
        self.status.configure(text=text.upper(), text_color=color)

    def progress_hook(self, d):
        """ This function handles the 1% to 100% calculation """
        if d['status'] == 'downloading':
            p = d.get('_percent_str', '0%').replace('%','')
            try:
                float_p = float(p) / 100
                self.progress_bar.set(float_p)
                self.progress_label.configure(text=f"{int(float(p))}%")
            except:
                pass
        elif d['status'] == 'finished':
            self.progress_bar.set(1)
            self.progress_label.configure(text="100%")

    def start_engine(self):
        url = self.url_var.get().strip()
        if not url: return
        
        # Reset UI
        self.progress_bar.set(0)
        self.progress_label.configure(text="0%")
        self.dl_btn.configure(state="disabled", text="WORKING...")
        
        threading.Thread(target=self.run_download, args=(url,), daemon=True).start()

    def run_download(self, url):
        self.update_status("🛰️ Bypassing Security...", "#00D084")
        is_mp3 = self.mode.get() == "MP3"
        
        ydl_opts = {
            'format': 'bestaudio/best' if is_mp3 else 'best',
            'progress_hooks': [self.progress_hook],
            'impersonate': 'chrome', 
            'nocheckcertificate': True,
            'quiet': True,
            'socket_timeout': 10,
        }

        if is_mp3:
            ydl_ # type: ignore