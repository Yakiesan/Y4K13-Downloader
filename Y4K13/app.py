import customtkinter as ctk
import yt_dlp
import threading
import os

# --- CORE DOWNLOADING LOGIC ---
def start_download():
    url = url_input.get()
    if not url:
        log.insert("end", "[-] ERROR: NO URL DETECTED\n", "red")
        return
    
    # Run in a thread so the UI doesn't freeze while downloading
    threading.Thread(target=dl_logic, args=(url,), daemon=True).start()

def dl_logic(url):
    log.insert("end", f"[*] INITIATING EXTRACTION: {url}\n")
    
    # yt-dlp settings
    options = {
        'format': 'best',
        'outtmpl': '%(title)s.%(ext)s',
        'quiet': True,
        'no_warnings': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([url])
        log.insert("end", "[+] DATA SUCCESSFULLY DOWNLOADED TO FOLDER\n", "green")
    except Exception as e:
        log.insert("end", f"[-] CRITICAL ERROR: {str(e)[:50]}...\n", "red")

# --- UI DESIGN (Y4K13 THEME) ---
ctk.set_appearance_mode("dark")
app = ctk.CTk()
app.title("Y4K13 ANYTO SYSTEM")
app.geometry("600x450")

# Heading
title = ctk.CTkLabel(app, text="Y4K13 DOWNLOADER v1.0", font=("Courier", 28, "bold"), text_color="#00FF00")
title.pack(pady=20)

# URL Input
url_input = ctk.CTkEntry(app, placeholder_text="PASTE URL (TIKTOK, IG, YT, ETC.)", 
                         width=480, height=40, fg_color="#001100", 
                         text_color="#00FF00", border_color="#00FF00")
url_input.pack(pady=10)

# Execute Button
btn = ctk.CTkButton(app, text="EXECUTE DOWNLOAD", font=("Courier", 16, "bold"),
                    fg_color="#006600", hover_color="#004400", 
                    text_color="white", width=200, height=45,
                    command=start_download)
btn.pack(pady=20)

# Console Log Box
log = ctk.CTkTextbox(app, width=550, height=180, fg_color="#000000", 
                     text_color="#00FF00", font=("Courier", 12),
                     border_width=1, border_color="#003300")
log.pack(pady=10)
log.insert("end", "[SYSTEM ONLINE] WAITING FOR TARGET URL...\n")

app.mainloop()