import customtkinter as ctk
from pytube import YouTube
import tkinter as tk
import threading

class MyGUI:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.geometry("600x400")  # Increased width
        self.download_status_var = tk.StringVar()
        self.download_status_var.set("Ready to Download")
        self.downloading = False
        self.done_window = None
        self.working_label = None
        self.create_widgets()
        self.root.bind("<Return>", lambda event: self.download_video())
        self.root.mainloop()

    def create_widgets(self):
        self.label = ctk.CTkLabel(self.root, text="YouTube Video Downloader", font=("Arial", 18))
        self.label.pack(padx=10, pady=10)

        self.url_label = ctk.CTkLabel(self.root, text="Video URL:", font=("Arial", 14))
        self.url_label.pack(padx=10, pady=5)

        self.url_entry = ctk.CTkEntry(self.root, font=("Arial", 16), width=400)
        self.url_entry.pack(padx=10, pady=10)

        self.location_label = ctk.CTkLabel(self.root, text="Download Folder:", font=("Arial", 14))
        self.location_label.pack(padx=10, pady=5)

        self.location_entry = ctk.CTkEntry(self.root, font=("Arial", 16), width=400)
        self.location_entry.pack(padx=10, pady=10)

        self.button = ctk.CTkButton(self.root, text="Download Video", font=('Arial', 18), command=self.download_video)
        self.button.pack(padx=10, pady=10)

        self.status_label = ctk.CTkLabel(self.root, textvariable=self.download_status_var, font=("Arial", 14))
        self.status_label.pack(padx=10, pady=5)

        self.working_label = ctk.CTkLabel(self.root, text="Working...", font=("Arial", 14))
        self.working_label.pack(pady=10)
        self.working_label.pack_forget()

    def download_video(self):
        video_url = self.url_entry.get().strip()
        download_location = self.location_entry.get().strip()

        if not self.downloading:
            threading.Thread(target=self.download_worker, args=(video_url, download_location)).start()

    def download_worker(self, video_url, download_location):
        try:
            self.downloading = True

            if self.working_label is None:
                self.working_label = ctk.CTkLabel(self.root, text="Working...", font=("Arial", 14))
                self.working_label.pack(pady=10)

            if self.working_label:
                self.working_label.pack()

            yt = YouTube(video_url)
            title = yt.title
            views = yt.views

            yd = yt.streams.get_highest_resolution()
            yd.download(download_location)

            self.show_done_window(download_location)

        except Exception as e:
            download_message = f'Download failed. Error: {str(e)}'
            print(download_message)

        finally:
            self.downloading = False

            if self.working_label:
                self.working_label.pack_forget()

    def show_done_window(self, download_location):
        if self.done_window:
            self.done_window.destroy()

        ctk.set_appearance_mode("dark")  # Set appearance mode to dark

        self.done_window = ctk.CTkToplevel(self.root)
        self.done_window.geometry("400x200")
        self.done_window.title("Download Done")

        done_label = ctk.CTkLabel(self.done_window, text="Download Complete!", font=("Arial", 18))
        done_label.pack(pady=20)

        back_button = ctk.CTkButton(self.done_window, text="Back to Download", font=('Arial', 14),
                                    command=lambda: self.back_to_download(download_location))
        back_button.pack(pady=20)

    def back_to_download(self, download_location):
        self.done_window.destroy()

        self.url_entry.delete(0, tk.END)
        self.location_entry.delete(0, tk.END)
        self.location_entry.insert(0, download_location)

        self.download_status_var.set("Ready to Download")

if __name__ == "__main__":
    app = MyGUI()
