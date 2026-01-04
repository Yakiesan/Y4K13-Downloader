import customtkinter as ctk
from yt_dlp import YoutubeDL
import os
import urllib.request

def download_content():
    url = url_entry.get()
    choice = format_option.get()
    
    if not url:
        status_label.configure(text="❌ Error: Paste a link first!", text_color="red")
        return

    status_label.configure(text=f"[*] Processing {choice}... Please wait.", text_color="yellow")
    root.update()

    # Base settings to look like a real person, not a bot
    ydl_opts = {
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'nocheckcertificate': True,
        'quiet': False,
        'no_warnings': False,
        'ignoreerrors': True,
        # This borrows your browser login to prove you are human:
        'cookiesfrombrowser': ('chrome',), 
    }

    try:
        if choice == "MP3 (Music)":
            ydl_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': '%(title)s.%(ext)s',
            })
        
        elif choice == "MP4 (Video)":
            ydl_opts.update({
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                'outtmpl': '%(title)s.%(ext)s',
            })

        elif choice == "PNG (Thumbnail)":
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                thumbnail_url = info['thumbnail']
                # Download image using standard python library
                file_name = f"{info['title']}.png".replace("/", "_") # Remove slashes from title
                urllib.request.urlretrieve(thumbnail_url, file_name)
                status_label.configure(text="✅ Success: PNG Saved!", text_color="green")
                return

        # Execute Download for MP3/MP4
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        status_label.configure(text=f"✅ Success: {choice} Downloaded!", text_color="green")

    except Exception as e:
        status_label.configure(text="❌ Error: YouTube Blocked this Request", text_color="red")
        print(f"Error Details: {e}")

# --- UI DESIGN ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Y4K13 Ultimate Downloader")
root.geometry("500x450")

# Title
title_label = ctk.CTkLabel(root, text="Y4K13 DOWNLOADER", font=("Impact", 35))
title_label.pack(pady=20)

# URL Input
url_entry = ctk.CTkEntry(root, placeholder_text="Paste YouTube URL here...", width=400, height=40)
url_entry.pack(pady=10)

# Format Selection Dropdown
format_label = ctk.CTkLabel(root, text="Select Format:")
format_label.pack()
format_option = ctk.CTkComboBox(root, values=["MP3 (Music)", "MP4 (Video)", "PNG (Thumbnail)"], width=200)
format_option.set("MP3 (Music)")
format_option.pack(pady=10)

# Download Button
btn_download = ctk.CTkButton(root, text="START DOWNLOAD", command=download_content, 
                             fg_color="#1f538d", hover_color="#14375e", width=200, height=45, font=("Arial", 14, "bold"))
btn_download.pack(pady=25)

# Status Label
status_label = ctk.CTkLabel(root, text="SYSTEM ONLINE", font=("Arial", 12))
status_label.pack(pady=10)

root.mainloop()