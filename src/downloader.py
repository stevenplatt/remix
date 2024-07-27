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

def trim_audio(file_path, start_time, end_time, output_path):
    print(f"Trimming {file_path} from {start_time} to {end_time}...")
    audio = AudioSegment.from_mp3(file_path)
    trimmed_audio = audio[start_time * 1000:end_time * 1000]  # times are in milliseconds
    trimmed_audio.export(output_path, format='mp3')

def combine_audios(audio_files, output_file='combined_audio.mp3', crossfade_duration=5000):
    combined = AudioSegment.empty()
    
    for index, audio_file in enumerate(audio_files):
        print(f"Adding {audio_file}...")
        audio = AudioSegment.from_mp3(audio_file)
        
        if index > 0:
            # Apply crossfade
            print(f"Applying {crossfade_duration / 1000} seconds crossfade...")
            combined = combined.append(audio, crossfade=crossfade_duration)
        else:
            combined += audio
    
    print(f"Saving combined audio to {output_file}...")
    combined.export(output_file, format='mp3')

def main(youtube_urls_time_ranges, output_folder='downloads', output_file='combined_audio.mp3'):
    # Download and trim audio files
    trimmed_files = []
    for url, (start_time, end_time) in youtube_urls_time_ranges:
        full_audio_path = download_audio(url, output_folder)
        trimmed_path = os.path.join(output_folder, f"trimmed_{os.path.basename(full_audio_path)}")
        trim_audio(full_audio_path, start_time, end_time, trimmed_path)
        trimmed_files.append(trimmed_path)
        os.remove(full_audio_path)  # Optionally remove the full audio file

    # Combine trimmed audio files with crossfade
    destination = os.path.join(output_folder, output_file)
    combine_audios(trimmed_files, destination)
    
    # Optionally, remove individual trimmed audio files
    for file in trimmed_files:
        os.remove(file)

# Example usage
youtube_urls_time_ranges = [
    ('https://www.youtube.com/watch?v=fTFS58mHJh8', (30, 90)),  # (start_time, end_time) in seconds
    ('https://www.youtube.com/watch?v=0habxsuXW4g', (15, 45))
]
main(youtube_urls_time_ranges)
