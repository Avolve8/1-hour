import os
import urllib.request
import moviepy.editor as mp
import youtube_dl
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_audio

def telecharger_audio_youtube(url):
    ydl_opts = {
        'outtmpl': 'download.mp3',
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '256',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        title = 'download'
    return title + '.mp3'

class VideoCreator:
    def __init__(self, audio_file, output_path):
        self.audio_file = audio_file
        self.output_path = output_path
    
    def create_video(self):
        # Crée une vidéo avec un fond noir d'une durée d'une heure
        duration = 3600  # Durée en secondes (1 heure)
        black_screen = mp.ColorClip(size=(256, 144), color=(0, 0, 0), duration=duration)
        
        # Charge la musique
        audio = mp.AudioFileClip(self.audio_file)
        
        # Vérifie si la durée de la musique dépasse la durée de la vidéo
        if audio.duration > duration:
            # Réduit la durée de la musique à la durée de la vidéo
            audio = audio.subclip(0, duration)
        else:
            # Boucle la musique pour qu'elle ait la même durée que la vidéo
            loops = int(duration / audio.duration)
            audio_clips = [audio] * loops
            audio = mp.concatenate_audioclips(audio_clips)
        
        # Ajoute la musique à la vidéo
        video = mp.concatenate_videoclips([black_screen.set_audio(audio)])
        
        # Sauvegarde la vidéo
        video.write_videofile(self.output_path, codec='libx264', audio_codec='aac', fps=10)


# Demande à l'utilisateur de saisir l'URL de la vidéo YouTube
url = input("Entrez l'URL de la vidéo YouTube : ")

# Télécharge l'audio de la vidéo
audio_file = telecharger_audio_youtube(url)

# Demande à l'utilisateur où il souhaite sauvegarder la vidéo
output_path = input("Entrez le chemin de sauvegarde de la vidéo (ex: /chemin/vers/dossier) : ")

creator = VideoCreator(audio_file, output_path)
creator.create_video()