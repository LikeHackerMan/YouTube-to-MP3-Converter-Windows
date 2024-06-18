from tkinter import Tk, Label, Entry, Button, messagebox, filedialog, OptionMenu, StringVar, Frame, BooleanVar
from tkinter import ttk
import os
import sys
import yt_dlp
import re

# Function to sanitize the filename by removing invalid characters
def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*\n\r\t]', '_', filename)

# Function to download and convert YouTube video to MP3
def download_video(url, output_folder, audio_quality, custom_filename=None):
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
        if custom_filename:
            base_filename = sanitize_filename(custom_filename)
        else:
            base_filename = sanitize_filename(info_dict['title'])
        file_path = os.path.join(output_folder, base_filename + '.mp3')
        original_file_path = ydl.prepare_filename(info_dict).replace('.webm', '.mp3').replace('.m4a', '.mp3')
        os.rename(original_file_path, file_path)
        return file_path

# Function to handle button click event for converting to MP3
def handle_convert_button():
    url = url_entry.get()
    
    output_folder = output_folder_var.get()
    if not output_folder:
        messagebox.showerror("Error", "Please select an output folder.")
        return

    audio_quality = selected_quality.get()
    custom_filename = None
    if custom_filename_var.get():
        custom_filename = filename_entry.get()
        if not custom_filename:
            messagebox.showerror("Error", "Please enter a filename or uncheck the custom filename option.")
            return
    
    try:
        # Download the video
        mp3_file_path = download_video(url, output_folder, audio_quality, custom_filename)
        
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

# Function to enable/disable filename entry based on checkbox
def toggle_filename_entry():
    if custom_filename_var.get():
        filename_entry.config(state="normal", bg="#34495E", fg="#ECF0F1")
    else:
        filename_entry.config(state="disabled", bg="#7F8C8D", fg="#BDC3C7")

# Function to exit the application
def exit_application():
    root.destroy()  # Properly closes the Tkinter application

# Create main window
root = Tk()
root.title("YouTube to MP3 Converter")
root.geometry("500x300")
root.configure(bg="#2C3E50")

style = ttk.Style()
style.configure("TLabel", background="#2C3E50", foreground="#ECF0F1", font=("Helvetica", 12))
style.configure("TButton", background="#3498DB", foreground="#ECF0F1", font=("Helvetica", 12))
style.configure("TCheckbutton", background="#2C3E50", foreground="#ECF0F1", font=("Helvetica", 12))
style.map("TButton", background=[('active', '#2980B9')], foreground=[('active', '#ECF0F1')])

# Create and place GUI components
frame = Frame(root, bg="#2C3E50")
frame.pack(padx=10, pady=10)

Label(frame, text="Enter YouTube URL:", bg="#2C3E50", fg="#ECF0F1", font=("Helvetica", 12)).grid(row=0, column=0, pady=5, sticky='w')
url_entry = Entry(frame, width=50, bg="#34495E", fg="#ECF0F1", insertbackground="#ECF0F1")
url_entry.grid(row=0, column=1, padx=5, pady=5)

custom_filename_var = BooleanVar()
custom_filename_check = ttk.Checkbutton(frame, text="Use custom filename", variable=custom_filename_var, command=toggle_filename_entry, style="TCheckbutton")
custom_filename_check.grid(row=1, column=0, pady=5, sticky='w', columnspan=2)

Label(frame, text="Enter File Name:", bg="#2C3E50", fg="#ECF0F1", font=("Helvetica", 12)).grid(row=2, column=0, pady=5, sticky='w')
filename_entry = Entry(frame, width=50, state="disabled", bg="#7F8C8D", fg="#BDC3C7", insertbackground="#ECF0F1")
filename_entry.grid(row=2, column=1, padx=5, pady=5)

Label(frame, text="Select Audio Quality:", bg="#2C3E50", fg="#ECF0F1", font=("Helvetica", 12)).grid(row=3, column=0, pady=5, sticky='w')
quality_options = ["128", "192", "256", "320"]
selected_quality = StringVar(frame)
selected_quality.set(quality_options[1])  # Default value set to "192"
quality_dropdown = OptionMenu(frame, selected_quality, *quality_options)
quality_dropdown.config(bg="#3498DB", fg="#ECF0F1", font=("Helvetica", 12))
quality_dropdown["menu"].config(bg="#3498DB", fg="#ECF0F1", font=("Helvetica", 12))
quality_dropdown.grid(row=3, column=1, padx=5, pady=5)

output_folder_var = StringVar(frame)

output_button = Button(frame, text="Select Output Folder", command=select_output_folder, bg="#3498DB", fg="#ECF0F1", activebackground="#2980B9", activeforeground="#ECF0F1")
output_button.grid(row=4, column=0, columnspan=2, pady=5)

convert_button = Button(frame, text="Convert to MP3", command=handle_convert_button, bg="#3498DB", fg="#ECF0F1", activebackground="#2980B9", activeforeground="#ECF0F1")
convert_button.grid(row=5, column=0, columnspan=2, pady=5)

exit_button = Button(frame, text="Exit", command=exit_application, bg="#E74C3C", fg="#ECF0F1", activebackground="#C0392B", activeforeground="#ECF0F1")
exit_button.grid(row=6, column=0, columnspan=2, pady=5)

# Run the main event loop
root.mainloop()
