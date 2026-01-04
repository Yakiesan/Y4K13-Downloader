import customtkinter as ctk
from yt_dlp import YoutubeDL
import threading
import os
from PIL import Image

class Y4K13App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Y4K13 ULTIMATE - MIKU EDITION")
        self.geometry("600x550")
        self.configure(fg_color="#000000")

        # --- MIKU IMAGE FIX ---
        # This looks for the image in the current folder
        self.img_name = "miku_peak.png"
        
        # UI Header
        self.header = ctk.CTkLabel(self, text="Y4K13 DOWNLOADER", font=("Impact", 45), text_color="#00FF41")
        self.header.pack(pady=(30, 0))
        
        self.status = ctk.CTkLabel(self, text="SYSTEM ONLINE", font=("Consolas", 12), text_color="#008F11")
        self.status.pack(pady=(0, 20))

        # URL Entry
        self.url_entry = ctk.CTkEntry(self, placeholder_text="Paste Link Here...", 
                                      width=450, height=50, border_color="#00FF41", fg_color="#0d0d0d")
        self.url_entry.pack(pady=10)

        # Format Dropdown
        self.mode = ctk.StringVar(value="MP3 (Music)")
        self.menu = ctk.CTkComboBox(self, values=["MP3 (Music)", "MP4 (Video)", "PNG (Thumbnail)"],
                                    variable=self.mode, width=200, height=40,
                                    button_color="#00FF41", border_color="#00FF41")
        self.menu.pack(pady=10)

        # Progress UI
        self.progress_bar = ctk.CTkProgressBar(self, width=400, progress_color="#00FF41")
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=15)

        # Download Button
        self.dl_btn = ctk.CTkButton(self, text="START EXTRACTION", command=self.start_thread,
                                    fg_color="#00FF41", hover_color="#008F11", text_color="black",
                                    font=("Arial", 18, "bold"), height=50)
        self.dl_btn.pack(pady=10)

        # --- MIKU PLACEMENT ---
        if os.path.exists(self.img_name):
            try:
                raw_img = Image.open(self.img_name)
                # Resize to fit corner nicely
                self.miku_img = ctk.CTkImage(light_image=raw_img, dark_image=raw_img, size=(280, 200))
                self.miku_label = ctk.CTkLabel(self, image=self.miku_img, text="")
                # Place her specifically in the bottom right corner
                self.miku_label.place(relx=1.0, rely=1.0, anchor="se")
                print("Miku loaded successfully!")
            except Exception as e:
                print(f"Miku Error: {e}")
        else:
            print("Miku image not found in folder. Make sure miku_peak.png is there!")

    def start_thread(self):
        threading.Thread(target=self.download_now, daemon=True).start()

    def download_now(self):
        url = self.url_entry.get()
        if not url: return
        
        self.status.configure(text="🛰️ BYPASSING BOT CHECK...", text_color="yellow")
        self.progress_bar.start()

        ydl_opts = {
            'format': 'bestaudio/best' if "MP3" in self.mode.get() else 'best',
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'nocheckcertificate': True,
        }

        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            self.status.configure(text="✅ SUCCESS!", text_color="#00FF41")
        except:
            self.status.configure(text="❌ FAILED", text_color="red")
        
        self.progress_bar.stop()
        self.progress_bar.set(1)

if __name__ == "__main__":
    app = Y4K13App()
    app.mainloop()