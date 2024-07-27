import yt_dlp
import os

def download_audio(youtube_url, output_folder='downloads'):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Define the options for yt-dlp
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_folder, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'noplaylist': True,
    }

    # Download audio
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        print(f"Downloading audio from {youtube_url}...")
        ydl.download([youtube_url])

    print("Download complete.")

# Example usage
youtube_url = 'https://www.youtube.com/watch?v=j69AZ7mfPlU'  # Replace with your YouTube video URL
download_audio(youtube_url)
