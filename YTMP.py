from tkinter import Tk, Label, Entry, Button, messagebox, filedialog, OptionMenu, StringVar
import os
import sys
import shutil
import yt_dlp
import re

# Function to sanitize the filename by removing invalid characters
def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*\n\r\t]', '_', filename)

# Function to download and convert YouTube video to MP3
def download_video(url, output_folder, audio_quality):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{output_folder}/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': audio_quality,
        }],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        file_path = ydl.prepare_filename(info_dict).replace('.webm', '.mp3').replace('.m4a', '.mp3')
        return file_path

# Function to handle button click event for converting to MP3
def handle_convert_button():
    url = url_entry.get()
    
    output_folder = output_folder_var.get()
    if not output_folder:
        messagebox.showerror("Error", "Please select an output folder.")
        return

    audio_quality = selected_quality.get()
    
    try:
        # Download the video
        mp3_file_path = download_video(url, output_folder, audio_quality)
        
        # Check if the video was downloaded successfully
        if not mp3_file_path or not os.path.exists(mp3_file_path):
            messagebox.showerror("Error", "Failed to download the video.")
            return

        messagebox.showinfo("Success", f"Downloaded and converted to MP3: {mp3_file_path}")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Function to handle button click event for selecting output folder
def select_output_folder():
    output_folder = filedialog.askdirectory()
    output_folder_var.set(output_folder)

# Function to exit the application
def exit_application():
    sys.exit()

# Create main window
root = Tk()
root.title("YouTube to MP3 Converter")

# Create and place GUI components
Label(root, text="Enter YouTube URL:").grid(row=0, column=0)
url_entry = Entry(root, width=50)
url_entry.grid(row=0, column=1, padx=5, pady=5)

Label(root, text="Enter File Name:").grid(row=1, column=0)
filename_entry = Entry(root, width=50)
filename_entry.grid(row=1, column=1, padx=5, pady=5)

Label(root, text="Select Audio Quality:").grid(row=2, column=0)
quality_options = ["128", "192", "256", "320"]
selected_quality = StringVar(root)
selected_quality.set(quality_options[1])  # Default value set to "192"
quality_dropdown = OptionMenu(root, selected_quality, *quality_options)
quality_dropdown.grid(row=2, column=1, padx=5, pady=5)

output_folder_var = StringVar(root)

output_button = Button(root, text="Select Output Folder", command=select_output_folder)
output_button.grid(row=3, column=0, columnspan=2, pady=5)

convert_button = Button(root, text="Convert to MP3", command=handle_convert_button)
convert_button.grid(row=4, column=0, columnspan=2, pady=5)

exit_button = Button(root, text="Exit", command=exit_application)
exit_button.grid(row=5, column=0, columnspan=2, pady=5)

# Run the main event loop
root.mainloop()
