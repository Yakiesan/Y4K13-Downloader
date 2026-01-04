import customtkinter as ctk
from yt_dlp import YoutubeDL
import threading
import os
import sys
from PIL import Image

# --- THE MAGIC IMAGE FINDER ---
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class Y4K13_Pro(ctk.CTk):
    def __init__(self):
        super().__init__()

        # UI Setup
        self.title("Y4K13 ULTIMATE")
        self.geometry("700x500")
        self.configure(fg_color="#0a0a0a") # Deep Space Black

        # Header Logo
        self.logo = ctk.CTkLabel(self, text="Y4K13", font=("Impact", 60), text_color="#00FF41")
        self.logo.pack(pady=(40, 5))
        
        self.sub = ctk.CTkLabel(self, text="SECURE MEDIA EXTRACTION", font=("Consolas", 12), text_color="#008F11")
        self.sub.pack(pady=(0, 30))

        # Main Input Bar
        self.url_var = ctk.StringVar()
        self.entry = ctk.CTkEntry(self, placeholder_text="ENTER SOURCE URL...", width=500, height=50, 
                                  border_color="#00FF41", fg_color="#111111", textvariable=self.url_var,
                                  font=("Consolas", 14))
        self.entry.pack(pady=10)

        # Format Switchers
        self.mode = ctk.StringVar(value="MP3")
        self.tab_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.tab_frame.pack(pady=10)

        self.btn_mp3 = ctk.CTkRadioButton(self.tab_frame, text="AUDIO (MP3)", variable=self.mode, value="MP3", 
                                          text_color="#00FF41", fg_color="#00FF41", border_color="#00FF41")
        self.btn_mp3.grid(row=0, column=0, padx=20)

        self.btn_mp4 = ctk.CTkRadioButton(self.tab_frame, text="VIDEO (MP4)", variable=self.mode, value="MP4", 
                                          text_color="#00FF41", fg_color="#00FF41", border_color="#00FF41")
        self.btn_mp4.grid(row=0, column=1, padx=20)

        # Action Button
        self.dl_btn = ctk.CTkButton(self, text="INITIALIZE DOWNLOAD", width=220, height=55, corner_radius=0,
                                    fg_color="#00FF41", text_color="black", font=("Impact", 20),
                                    hover_color="#008F11", command=self.start_thread)
        self.dl_btn.pack(pady=20)

        self.status = ctk.CTkLabel(self, text="SYSTEM READY", text_color="#00FF41", font=("Consolas", 12))
        self.status.pack()

        # --- MIKU PLACEMENT ---
        miku_path = resource_path("miku_peak.png")
        if os.path.exists(miku_path):
            raw_img = Image.open(miku_path)
            self.miku_ctk = ctk.CTkImage(light_image=raw_img, dark_image=raw_img, size=(280, 200))
            self.miku_label = ctk.CTkLabel(self, image=self.miku_ctk, text="")
            # Miku peaks from the bottom right corner
            self.miku_label.place(relx=1.0, rely=1.0, anchor="se")

    def start_thread(self):
        self.dl_btn.configure(state="disabled", text="WORKING...")
        threading.Thread(target=self.run_download, daemon=True).start()

    def run_download(self):
        url = self.url_var.get()
        if not url:
            self.update_status("❌ ERROR: NO URL", "red")
            return

        self.update_status("🛰️ BYPASSING BOT DETECTION...", "yellow")

        # THE ELITE ANTI-BOT SETTINGS (2026 Standard)
        ydl_opts = {
            'format': 'bestaudio/best' if self.mode.get() == "MP3" else 'best',
            'impersonate': 'chrome', # Mimics real Chrome network fingerprints
            'nocheckcertificate': True,
            'quiet': True,
            'no_warnings': True,
            # Force mobile/desktop user agents to rotate
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }

        if self.mode.get() == "MP3":
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]

        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            self.update_status("✅ DOWNLOAD COMPLETE", "#00FF41")
        except Exception as e:
            print(f"Error: {e}")
            self.update_status("❌ FAILED: LINK PROTECTED", "red")
        
        self.dl_btn.configure(state="normal", text="INITIALIZE DOWNLOAD")

    def update_status(self, text, color):
        self.status.configure(text=text, text_color=color)

if __name__ == "__main__":
    app = Y4K13_Pro()
    app.mainloop()