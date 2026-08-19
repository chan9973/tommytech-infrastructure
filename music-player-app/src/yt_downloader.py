"""
YouTube Music Downloader
Download audio from YouTube and convert to FLAC, MP3, or WAV
"""
import os
import tempfile
import shutil
from pathlib import Path
from typing import Optional
from pydub import AudioSegment

try:
    from pytube import YouTube
    from pytube.exceptions import PytubeError
except ImportError:
    YouTube = None
    PytubeError = Exception


class YouTubeDownloader:
    """Download YouTube audio files"""
    
    def __init__(self):
        if YouTube is None:
            raise ImportError("pytube not installed. Run: pip install pytube")
    
    def _get_safe_temp_dir(self) -> str:
        """Get a user-writable temp directory"""
        # Try user's temp first
        user_temp = os.path.expanduser("~/AppData/Local/Temp")
        if os.access(user_temp, os.W_OK):
            return user_temp
        
        # Fallback to system temp
        return tempfile.gettempdir()
    
    def download(
        self, 
        url: str, 
        format_type: str = "mp3",
        output_dir: Optional[str] = None
    ) -> str:
        """
        Download YouTube video and extract audio
        
        Args:
            url: YouTube video URL
            format_type: Output format (flac, mp3, or wav)
            output_dir: Output directory (default: Downloads/music)
        
        Returns:
            Path to downloaded file
        """
        if output_dir is None:
            output_dir = os.path.join(os.path.expanduser("~"), "Downloads", "music")
        
        os.makedirs(output_dir, exist_ok=True)
        
        # Download video
        yt = YouTube(url)
        title = yt.title.replace("/", "_").replace("\\", "_")[:50]
        
        # Get audio-only stream
        stream = yt.streams.filter(only_audio=True).first()
        if not stream:
            raise ValueError("Could not find audio stream")
        
        # Download to user-writable temp file
        safe_temp = self._get_safe_temp_dir()
        temp_file = stream.download(output_path=safe_temp, filename="temp_audio_yt")
        
        # Convert to desired format
        output_file = os.path.join(output_dir, f"{title}.{format_type}")
        
        audio = AudioSegment.from_file(temp_file)
        
        # Export with appropriate parameters
        export_params = {
            'flac': {'codec': 'flac'},
            'mp3': {'codec': 'libmp3lame', 'bitrate': '320k'},
            'wav': {'codec': 'pcm_s16le'}
        }.get(format_type, {'codec': format_type})
        
        audio.export(output_file, format=format_type, **export_params)
        
        # Cleanup temp file
        try:
            os.unlink(temp_file)
        except Exception:
            pass  # Ignore cleanup errors
        
        return output_file
    
    def get_video_info(self, url: str) -> dict:
        """Get video information without downloading"""
        yt = YouTube(url)
        return {
            'title': yt.title,
            'author': yt.author,
            'length': yt.length,
            'views': yt.views
        }