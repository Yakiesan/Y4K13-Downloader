import customtkinter as ctk
from yt_dlp import YoutubeDL
import os

def download_content():
    url = url_entry.get()
    choice = format_option.get() # Gets MP3, MP4, or PNG
    
    if not url:
        status_label.configure(text="Error: Paste a link first!", text_color="red")
        return

    status_label.configure(text=f"[*] Processing {choice}...", text_color="yellow")
    root.update()

    # --- THE MAGIC SETTINGS ---
    ydl_opts = {
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'nocheckcertificate': True,
        'quiet': False,
        'no_warnings': False,
    }

    try:
        if choice == "MP3 (Music)":
            ydl_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}],
                'outtmpl': '%(title)s.%(ext)s',
            })
        
        elif choice == "MP4 (Video)":
            ydl_opts.update({
                'format': 'best[ext=mp4]',
                'outtmpl': '%(title)s.%(ext)s',
            })

        elif choice == "PNG (Thumbnail)":
            # For thumbnails, we just get the info and download the image
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                thumbnail_url = info['thumbnail']
                import urllib.request
                urllib.request.urlretrieve(thumbnail_url, f"{info['title']}.png")
                status_label.configure(text="Success: PNG Saved!", text_color="green")
                return

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        status_label.configure(text=f"Success: {choice} Downloaded!", text_color="green")

    except Exception as e:
        status_label.configure(text=f"Error: Check link or Bot block", text_color="red")
        print(f"Details: {e}")

# --- UI SETUP ---
ctk.set_appearance_mode("dark")
root = ctk.CTk()
root.title("Y4K13 Ultimate Downloader")
root.geometry("500x400")

label = ctk.CTkLabel(root, text="Y4K13 Downloader", font=("Arial", 24, "bold"))
label.pack(pady=20)

url_entry = ctk.CTkEntry(root, placeholder_text="Paste YouTube Link Here...", width=400)
url_entry.pack(pady=10)

# The Dropdown for MP3, MP4, or PNG
format_option = ctk.CTkComboBox(root, values=["MP3 (Music)", "MP4 (Video)", "PNG (Thumbnail)"], width=200)
format_option.set("MP3 (Music)")
format_option.pack(pady=10)

download_button = ctk.CTkButton(root, text="START DOWNLOAD", command=download_content, fg_color="green", hover_color="darkgreen")
download_button.pack(pady=20)

status_label = ctk.CTkLabel(root, text="Waiting for Target URL...", text_color="gray")
status_label.pack(pady=10)

root.mainloop()