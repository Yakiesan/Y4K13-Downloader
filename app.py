import customtkinter as ctk
from yt_dlp import YoutubeDL
import threading
import urllib.request
import os

# Fail-safe for the image library
try:
    from PIL import Image
    PIL_INSTALLED = True
except ImportError:
    PIL_INSTALLED = False

class Y4K13App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Setup
        self.title("Y4K13 Ultimate Downloader")
        self.geometry("600x500")
        self.configure(fg_color="#0a0a0a") # Cyberpunk Black

        # Download Miku background if it doesn't exist
        self.miku_path = "miku_bg.png"
        if not os.path.exists(self.miku_path):
            try:
                # Peaking Miku URL
                miku_url = "https://i.imgur.com/39hN7m0.png" 
                urllib.request.urlretrieve(miku_url, self.miku_path)
            except: pass

        # --- UI ELEMENTS ---
        
        # Miku Image (Peaking from the bottom right)
        if PIL_INSTALLED:
            try:
                self.raw_img = Image.open(self.miku_path)
                self.miku_img = ctk.CTkImage(self.raw_img, size=(220, 220))
                self.miku_label = ctk.CTkLabel(self, image=self.miku_img, text="")
                self.miku_label.place(relx=1.0, rely=1.0, anchor="se") 
            except: pass

        # Header Section
        self.title_label = ctk.CTkLabel(self, text="Y4K13 DOWNLOADER", 
                                        font=("Arial", 32, "bold"), text_color="#2ecc71")
        self.title_label.pack(pady=(40, 5))
        
        self.sub_label = ctk.CTkLabel(self, text="SYSTEM STATUS: ONLINE", font=("Arial", 10), text_color="#27ae60")
        self.sub_label.pack(pady=(0, 20))

        # Input Field
        self.url_entry = ctk.CTkEntry(self, placeholder_text="Paste YouTube URL here...", 
                                      width=420, height=45, border_color="#2ecc71",
                                      fg_color="#1a1a1a", text_color="white")
        self.url_entry.pack(pady=10)

        # Dropdown Menu
        self.format_var = ctk.StringVar(value="MP3 (Music)")
        self.format_menu = ctk.CTkComboBox(self, values=["MP3 (Music)", "MP4 (Video)", "PNG (Thumbnail)"],
                                           variable=self.format_var, width=200, height=35,
                                           button_color="#2ecc71", border_color="#2ecc71",
                                           dropdown_fg_color="#1a1a1a")
        self.format_menu.pack(pady=10)

        # Progress Bar
        self.progress = ctk.CTkProgressBar(self, width=400, progress_color="#2ecc71", fg_color="#1a1a1a")
        self.progress.set(0)
        self.progress.pack(pady=20)

        # Main Action Button
        self.btn = ctk.CTkButton(self, text="⚡ START EXTRACTION ⚡", command=self.start_thread,
                                 fg_color="#2ecc71", hover_color="#27ae60", 
                                 text_color="black", font=("Arial", 16, "bold"), height=50, width=250)
        self.btn.pack(pady=10)

        # Status Label
        self.status = ctk.CTkLabel(self, text="READY FOR TARGET URL", text_color="#2ecc71", font=("Consolas", 12))
        self.status.pack(pady=10)

    def start_thread(self):
        # Prevent app freeze using threading
        thread = threading.Thread(target=self.download_logic, daemon=True)
        thread.start()

    def download_logic(self):
        url = self.url_entry.get()
        choice = self.format_var.get()
        
        if not url:
            self.status.configure(text="❌ INPUT REQUIRED", text_color="#e74c3c")
            return

        self.status.configure(text="🛰️ BYPASSING PROTOCOLS...", text_color="#f1c40f")
        self.btn.configure(state="disabled")
        self.progress.start()

        # Modern Stealth Settings
        ydl_opts = {
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'nocheckcertificate': True,
            'cookiesfrombrowser': ('chrome',), # Change to 'edge' if needed
            'quiet': True,
            'no_warnings': True,
        }

        try:
            if "MP3" in choice:
                ydl_opts.update({
                    'format': 'bestaudio/best',
                    'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '192'}],
                    'outtmpl': '%(title)s.%(ext)s'
                })
            elif "MP4" in choice:
                ydl_opts.update({
                    'format': 'best[ext=mp4]',
                    'outtmpl': '%(title)s.%(ext)s'
                })
            elif "PNG" in choice:
                with YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    urllib.request.urlretrieve(info['thumbnail'], f"{info['title']}.png")
                self.finish_download("✅ THUMBNAIL SAVED!")
                return
            
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            self.finish_download("✅ DOWNLOAD SUCCESS!")

        except Exception as e:
            self.status.configure(text="⚠️ BOT DETECTION ACTIVE", text_color="#e74c3c")
            print(f"Log: {e}")
            self.btn.configure(state="normal")
            self.progress.stop()

    def finish_download(self, message):
        self.status.configure(text=message, text_color="#2ecc71")
        self.progress.stop()
        self.progress.set(1)
        self.btn.configure(state="normal")

if __name__ == "__main__":
    app = Y4K13App()
    app.mainloop()