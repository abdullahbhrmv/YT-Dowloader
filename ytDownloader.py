import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from yt_dlp import YoutubeDL
import threading
import os

class YouTubeDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Video Downloader")
        self.root.geometry("600x400")
        self.root.configure(padx=20, pady=20)

        # URL Entry
        url_frame = ttk.LabelFrame(root, text="Video URL", padding="10")
        url_frame.pack(fill="x", pady=(0, 10))
        
        self.url_entry = ttk.Entry(url_frame, width=50)
        self.url_entry.pack(fill="x", pady=5)

        # Download Location
        location_frame = ttk.LabelFrame(root, text="Download Location", padding="10")
        location_frame.pack(fill="x", pady=(0, 10))
        
        self.location_entry = ttk.Entry(location_frame, width=50)
        self.location_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        browse_btn = ttk.Button(location_frame, text="Browse", command=self.browse_location)
        browse_btn.pack(side="right")

        # Download Button
        self.download_btn = ttk.Button(root, text="Download Video", command=self.start_download)
        self.download_btn.pack(pady=10)

        # Progress Bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(root, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill="x", pady=10)

        # Status Label
        self.status_label = ttk.Label(root, text="Ready to download")
        self.status_label.pack(pady=5)

        # Set default download location
        default_path = os.path.join(os.path.expanduser("~"), "Downloads")
        self.location_entry.insert(0, default_path)

    def browse_location(self):
        directory = filedialog.askdirectory()
        if directory:
            self.location_entry.delete(0, tk.END)
            self.location_entry.insert(0, directory)

    def update_progress(self, d):
        if d['status'] == 'downloading':
            try:
                # Calculate percentage
                percent = (d['downloaded_bytes'] / d['total_bytes']) * 100
                self.progress_var.set(percent)
                self.status_label.config(text=f"Downloading: {percent:.1f}%")
                self.root.update()
            except:
                pass

    def download_video(self):
        try:
            url = self.url_entry.get()
            if not url:
                messagebox.showerror("Error", "Please enter a YouTube URL")
                return

            download_path = self.location_entry.get()
            if not os.path.exists(download_path):
                os.makedirs(download_path)

            ydl_opts = {
                'format': 'bestvideo[height=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080][ext=mp4]/best',
                'merge_output_format': 'mp4',
                'quiet': False,
                'no_warnings': False,
                'progress_hooks': [self.update_progress],
                'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
            }

            self.download_btn.config(state="disabled")
            self.status_label.config(text="Starting download...")
            
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            self.status_label.config(text="Download completed successfully!")
            messagebox.showinfo("Success", "Video downloaded successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.status_label.config(text="Download failed")

        finally:
            self.download_btn.config(state="normal")
            self.progress_var.set(0)

    def start_download(self):
        # Start download in a separate thread to prevent GUI freezing
        thread = threading.Thread(target=self.download_video)
        thread.daemon = True
        thread.start()

if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeDownloaderApp(root)
    root.mainloop()
