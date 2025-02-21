import yt_dlp
import tkinter as tk
from tkinter import messagebox, ttk
import os
import subprocess

# Define internal storage path
INTERNAL_STORAGE_PATH = "/storage/emulated/0/Download"

# Ensure the directory exists
if not os.path.exists(INTERNAL_STORAGE_PATH):
    os.makedirs(INTERNAL_STORAGE_PATH)

def refresh_gallery(file_path):
    """Refresh the gallery to display the downloaded video"""
    try:
        subprocess.run(["am", "broadcast", "-a", "android.intent.action.MEDIA_SCANNER_SCAN_FILE", "-d", f"file://{file_path}"], check=True)
    except Exception as e:
        print(f"Error refreshing gallery: {e}")

def download_video(video_url, format_choice):
    """Download the video to internal storage"""
    status_label.config(text="📥 Downloading...", fg="yellow")
    progress_bar.start(10)
    root.update_idletasks()
    
    options = {
        'outtmpl': f'{INTERNAL_STORAGE_PATH}/%(title)s.%(ext)s',
        'progress_hooks': [progress_hook]
    }
    if format_choice == "Audio Only":
        options['format'] = 'bestaudio/best'
        options['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    else:
        options['format'] = format_choice
    
    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(video_url, download=True)
            file_name = ydl.prepare_filename(info)
        
        # Refresh gallery after download
        refresh_gallery(file_name)
        
        progress_bar.stop()
        status_label.config(text="✅ Download Successful!", fg="green")
        messagebox.showinfo("Success", f"✅ Video downloaded to: {INTERNAL_STORAGE_PATH}")
    except Exception as e:
        progress_bar.stop()
        status_label.config(text="❌ Download Failed", fg="red")
        messagebox.showerror("Error", f"❌ An error occurred: {e}")

def progress_hook(d):
    """Update progress bar during download"""
    if d['status'] == 'downloading':
        percent = d.get('downloaded_bytes', 0) / d.get('total_bytes', 1) * 100
        progress_bar['value'] = percent
        root.update_idletasks()

def start_download():
    """Start the download process"""
    url = url_entry.get()
    if url:
        format_choice = quality_var.get()
        download_video(url, format_choice)
    else:
        messagebox.showwarning("⚠️ Warning", "Please enter a video URL!")

# Create application window
root = tk.Tk()
root.title("Mohamed Zidan Downloader")
root.geometry("400x400")
root.configure(bg="#222")

# Application title with colors
title_label = tk.Label(root, text="Mohamed Zidan Downloader", font=("Arial", 12, "bold"), fg="magenta", bg="#222")
title_label.pack(pady=10)

tk.Label(root, text="🎬 Enter video URL:", font=("Arial", 14), fg="white", bg="#222").pack(pady=5)
url_entry = tk.Entry(root, width=40, font=("Arial", 12), bg="#333", fg="white")
url_entry.pack(pady=5)

tk.Label(root, text="🔽 Select Quality:", font=("Arial", 14), fg="white", bg="#222").pack(pady=10)
quality_var = tk.StringVar(value="best")
quality_menu = tk.OptionMenu(root, quality_var, "best", "worst", "Audio Only")
quality_menu.pack()

tk.Button(root, text="⬇️ Download", font=("Arial", 14), bg="#0a84ff", fg="white", command=start_download).pack(pady=20)

progress_bar = ttk.Progressbar(root, length=300, mode='determinate')
progress_bar.pack(pady=10)

status_label = tk.Label(root, text="", font=("Arial", 12), fg="white", bg="#222")
status_label.pack(pady=10)

root.mainloop()
