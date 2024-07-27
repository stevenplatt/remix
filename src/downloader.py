import os
from yt_dlp import YoutubeDL
from pydub import AudioSegment

def download_audio(youtube_url, output_folder='downloads'):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
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

    with YoutubeDL(ydl_opts) as ydl:
        print(f"Downloading audio from {youtube_url}...")
        info = ydl.extract_info(youtube_url, download=True)
        return os.path.join(output_folder, f"{info['title']}.mp3")

def combine_audios(audio_files, output_file='combined_audio.mp3'):
    combined = AudioSegment.empty()
    for audio_file in audio_files:
        print(f"Adding {audio_file}...")
        audio = AudioSegment.from_mp3(audio_file)
        combined += audio
    
    print(f"Saving combined audio to {output_file}...")
    combined.export(output_file, format='mp3')

def main(youtube_urls, output_folder='downloads', output_file='combined_audio.mp3'):
    # Download audio files
    audio_files = [download_audio(url, output_folder) for url in youtube_urls]
    
    # Combine audio files
    destination = output_folder + '/' + output_file
    combine_audios(audio_files, destination)
    
    # Optionally, remove individual audio files
    for file in audio_files:
        os.remove(file)

# Example usage
youtube_urls = [
    'https://www.youtube.com/watch?v=fTFS58mHJh8',  # Replace with your YouTube video URLs
    'https://www.youtube.com/watch?v=0habxsuXW4g'
]
main(youtube_urls)
