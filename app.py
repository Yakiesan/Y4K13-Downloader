import customtkinter as ctk
from yt_dlp import YoutubeDL
import threading
import urllib.request
import os
from PIL import Image

class Y4K13App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Setup
        self.title("Y4K13 Ultimate Downloader")
        self.geometry("600x500")
        self.configure(fg_color="#0a0a0a") # Deep black background

        # Download Miku background if it doesn't exist
        self.miku_path = "miku_bg.png"
        if not os.path.exists(self.miku_path):
            try:
                # Using a cute Miku peaking image URL
                miku_url = "https://i.imgur.com/39hN7m0.png" 
                urllib.request.urlretrieve(miku_url, self.miku_path)
            except: pass

        # --- UI ELEMENTS ---
        
        # Miku Image (Peaking from the bottom)
        try:
            self.miku_img = ctk.CTkImage(Image.open(self.miku_path), size=(200, 200))
            self.miku_label = ctk.CTkLabel(self, image=self.miku_img, text="")
            self.miku_label.place(relx=1.0, rely=1.0, anchor="se") # Bottom Right
        except: pass

        # Title with Green Glow
        self.title_label = ctk.CTkLabel(self, text="Y4K13 DOWNLOADER", 
                                        font=("Orbitron", 32, "bold"), text_color="#2ecc71")
        self.title_label.pack(pady=30)

        # Input Field
        self.url_entry = ctk.CTkEntry(self, placeholder_text="Paste Link Here...", 
                                      width=400, height=45, border_color="#2ecc71",
                                      fg_color="#1a1a1a")
        self.url_entry.pack(pady=10)

        # Dropdown
        self.format_var = ctk.StringVar(value="MP3 (Music)")
        self.format_menu = ctk.CTkComboBox(self, values=["MP3 (Music)", "MP4 (Video)", "PNG (Thumbnail)"],
                                           variable=self.format_var, width=200, height=35,
                                           button_color="#2ecc71", border_color="#2ecc71")
        self.format_menu.pack(pady=10)

        # Animated Progress Bar (Starts hidden)
        self.progress = ctk.CTkProgressBar(self, width=400, progress_color="#2ecc71")
        self.progress.set(0)
        self.progress.pack(pady=20)

        # Download Button
        self.btn = ctk.CTkButton(self, text="DOWNLOAD NOW", command=self.start_thread,
                                 fg_color="#2ecc71", hover_color="#27ae60", 
                                 text_color="black", font=("Arial", 16, "bold"), height=50)
        self.btn.pack(pady=10)

        # Status
        self.status = ctk.CTkLabel(self, text="READY TO ROCK", text_color="#2ecc71")
        self.status.pack(pady=10)

    def start_thread(self):
        # Starts download in background so window doesn't freeze
        thread = threading.Thread(target=self.download_logic)
        thread.start()

    def download_logic(self):
        url = self.url_entry.get()
        choice = self.format_var.get()
        
        if not url:
            self.status.configure(text="⚠️ PASTE A LINK!", text_color="red")
            return

        self.status.configure(text="🌀 INITIATING BYPASS...", text_color="#2ecc71")
        self.btn.configure(state="disabled")
        self.progress.start() # Start animation

        ydl_opts = {
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'nocheckcertificate': True,
            'cookiesfrombrowser': ('chrome',), # Bypasses Bot Check
            'quiet': True,
        }

        try:
            if "MP3" in choice:
                ydl_opts.update({'format': 'bestaudio/best', 'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '192'}]})
            elif "MP4" in choice:
                ydl_opts.update({'format': 'best[ext=mp4]'})
            
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            self.status.configure(text="✅ DOWNLOAD COMPLETE!", text_color="#2ecc71")
        except Exception as e:
            self.status.configure(text="❌ YOUTUBE BLOCKED THE BOT", text_color="red")
            print(f"Error: {e}")
        
        self.progress.stop()
        self.progress.set(1)
        self.btn.configure(state="normal")

if __name__ == "__main__":
    app = Y4K13App()
    app.mainloop()