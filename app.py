import customtkinter as ctk
from yt_dlp import YoutubeDL
import threading
import urllib.request
import os
from PIL import Image

class Y4K13App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Config
        self.title("Y4K13 ALL-IN-ONE DOWNLOADER")
        self.geometry("650x550")
        self.configure(fg_color="#000000")

        # --- MIKU IMAGE LOGIC ---
        self.miku_path = "miku_peak.png"
        self.load_miku()

        # --- UI DESIGN ---
        # Title
        self.header = ctk.CTkLabel(self, text="Y4K13 DOWNLOADER", font=("Impact", 40), text_color="#00FF41")
        self.header.pack(pady=(30, 0))
        
        self.sub = ctk.CTkLabel(self, text="MULTI-PLATFORM BYPASS ACTIVE", font=("Arial", 12), text_color="#008F11")
        self.sub.pack(pady=(0, 20))

        # Link Entry
        self.url_entry = ctk.CTkEntry(self, placeholder_text="Paste Link (YouTube, TikTok, Instagram...)", 
                                      width=450, height=50, border_color="#00FF41", fg_color="#0d0d0d")
        self.url_entry.pack(pady=10)

        # Dropdown
        self.mode = ctk.StringVar(value="MP3 (Music)")
        self.menu = ctk.CTkComboBox(self, values=["MP3 (Music)", "MP4 (Video)", "PNG (Thumbnail)"],
                                    variable=self.mode, width=220, height=40,
                                    button_color="#00FF41", border_color="#00FF41")
        self.menu.pack(pady=10)

        # Progress
        self.progress = ctk.CTkProgressBar(self, width=450, progress_color="#00FF41", fg_color="#1a1a1a")
        self.progress.set(0)
        self.progress.pack(pady=20)

        # Button
        self.dl_btn = ctk.CTkButton(self, text="GET CONTENT", command=self.start_thread,
                                    fg_color="#00FF41", hover_color="#008F11", text_color="black",
                                    font=("Arial", 18, "bold"), height=55, width=250)
        self.dl_btn.pack(pady=10)

        # Status
        self.status = ctk.CTkLabel(self, text="SYSTEM READY", text_color="#00FF41", font=("Consolas", 13))
        self.status.pack(pady=10)

        # Miku Label (Placement)
        if hasattr(self, 'miku_img'):
            self.miku_label = ctk.CTkLabel(self, image=self.miku_img, text="")
            self.miku_label.place(relx=1.0, rely=1.0, anchor="se")

    def load_miku(self):
        # High-quality peaking Miku
        url = "https://i.imgur.com/39hN7m0.png"
        if not os.path.exists(self.miku_path):
            try: urllib.request.urlretrieve(url, self.miku_path)
            except: pass
        
        if os.path.exists(self.miku_path):
            try:
                img = Image.open(self.miku_path)
                self.miku_img = ctk.CTkImage(light_image=img, dark_image=img, size=(250, 250))
            except: pass

    def start_thread(self):
        threading.Thread(target=self.download_now, daemon=True).start()

    def download_now(self):
        url = self.url_entry.get()
        choice = self.mode.get()
        
        if not url:
            self.status.configure(text="❌ NO LINK DETECTED")
            return

        self.status.configure(text="🛰️ SPOOFING MOBILE CLIENT...", text_color="#f1c40f")
        self.dl_btn.configure(state="disabled")
        self.progress.start()

        # THE "MOBILE SPOOF" - Bypass Bot detection without Chrome
        ydl_opts = {
            'format': 'bestaudio/best' if "MP3" in choice else 'bestvideo+bestaudio/best',
            'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1',
            'nocheckcertificate': True,
            'quiet': True,
            'ignoreerrors': True,
            'no_warnings': True,
            'referer': 'https://www.youtube.com/',
        }

        if "MP3" in choice:
            ydl_opts['postprocessors'] = [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '192'}]

        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            self.status.configure(text="✅ EXTRACTION COMPLETE", text_color="#00FF41")
        except Exception as e:
            self.status.configure(text="❌ SECURITY BLOCK", text_color="red")
        
        self.progress.stop()
        self.progress.set(1)
        self.dl_btn.configure(state="normal")

if __name__ == "__main__":
    app = Y4K13App()
    app.mainloop()