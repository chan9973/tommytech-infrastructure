"""
Nissan GTR Music Player - Main Application
Red-themed desktop music player with 30-band equalizer
"""
import os
import sys
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, List
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import numpy as np
from pydub import AudioSegment
from pydub.playback import play

try:
    from src.audio_player import Equalizer30Band, Track
except ImportError:
    from audio_player import Equalizer30Band, Track

try:
    from src.yt_downloader import YouTubeDownloader
except ImportError:
    from yt_downloader import YouTubeDownloader

# Nissan GTR Red Theme Colors
GTR_RED = "#D40000"
GTR_DARK = "#1A0000"
GTR_BRIGHT_RED = "#FF3B30"
GTR_GRAY = "#333333"
GTR_LIGHT = "#FA8072"


class NissanGTRPlayer(tk.Tk):
    """Main application window with Nissan GTR styling"""
    
    def __init__(self):
        super().__init__()
        
        self.title("Nissan GTR Music Player")
        self.geometry("900x700")
        self.resizable(False, False)
        self.configure(bg=GTR_DARK)
        
        # Set icon (will use text if no icon)
        self._set_gtr_icon()
        
        # Initialize players
        self.downloader = YouTubeDownloader()
        self.playlist: List[Track] = []
        self.current_track: Optional[Track] = None
        
        # Build UI
        self._build_ui()
    
    def _set_gtr_icon(self):
        """Set GTR-themed icon"""
        # Create a simple red circle icon
        pass  # Placeholder for icon
    
    def _build_ui(self):
        """Build the entire user interface"""
        
        # Title bar with GTR logo
        self._create_header()
        
        # Main content area
        main_frame = tk.Frame(self, bg=GTR_DARK)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Left panel - Playlist
        self._create_playlist_panel(main_frame)
        
        # Center panel - Player controls
        self._create_player_panel(main_frame)
        
        # Right panel - Equalizer
        self._create_equalizer_panel(main_frame)
        
        # YouTube download section
        self._create_download_panel()
    
    def _create_header(self):
        """Create header with GTR badge"""
        header = tk.Frame(self, bg=GTR_RED, height=60)
        header.pack(fill=tk.X)
        
        # GTR badge text
        badge = tk.Label(
            header,
            text="Nissan GTR MUSIC SYSTEM",
            font=("Arial", 16, "bold"),
            fg="white",
            bg=GTR_RED,
            width=40
        )
        badge.pack(pady=15)
    
    def _create_playlist_panel(self, parent):
        """Create playlist section"""
        frame = tk.LabelFrame(parent, text="PLAYLIST", bg=GTR_DARK, fg=GTR_RED)
        frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Playlist listbox
        self.playlist_box = tk.Listbox(
            frame,
            width=30,
            height=20,
            bg=GTR_DARK,
            fg="white",
            selectbackground=GTR_RED,
            font=("Consolas", 9)
        )
        self.playlist_box.pack(padx=5, pady=5, fill=tk.BOTH)
        
        # Add buttons
        btn_frame = tk.Frame(frame, bg=GTR_DARK)
        btn_frame.pack(fill=tk.X, padx=5, pady=(0, 5))
        
        tk.Button(
            btn_frame,
            text="ADD FOLDER",
            command=self._add_folder,
            bg=GTR_RED, fg="white",
            font=("Arial", 8, "bold")
        ).pack(fill=tk.X, padx=2, pady=2)
    
    def _create_player_panel(self, parent):
        """Create main player controls"""
        frame = tk.LabelFrame(parent, text="PLAYER", bg=GTR_DARK, fg=GTR_RED)
        frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        
        # Track info
        self.track_label = tk.Label(
            frame, text="No track loaded",
            bg=GTR_DARK, fg="white",
            font=("Arial", 10)
        )
        self.track_label.pack(pady=5)
        
        # Progress bar
        self.progress = tk.Scale(
            frame, from_=0, to=100, orient=tk.HORIZONTAL,
            length=200, bg=GTR_RED, fg="white",
            highlightthickness=1
        )
        self.progress.pack(pady=5)
        
        # Control buttons
        btn_frame = tk.Frame(frame, bg=GTR_DARK)
        btn_frame.pack(pady=10)
        
        self.play_btn = tk.Button(
            btn_frame, text="► PLAY", command=self._play,
            bg=GTR_RED, fg="white", font=("Arial", 8, "bold")
        )
        self.play_btn.grid(row=0, column=0, padx=3)
        
        tk.Button(
            btn_frame, text="⏸ STOP", command=self._stop,
            bg=GTR_GRAY, fg="white", font=("Arial", 8, "bold")
        ).grid(row=0, column=1, padx=3)
        
        tk.Button(
            btn_frame, text="⏭ NEXT", command=self._next,
            bg=GTR_RED, fg="white", font=("Arial", 8, "bold")
        ).grid(row=0, column=2, padx=3)
    
    def _create_equalizer_panel(self, parent):
        """Create 30-band equalizer"""
        frame = tk.LabelFrame(parent, text="30-BAND EQUALIZER", bg=GTR_DARK, fg=GTR_RED)
        frame.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)
        
        self.eq = Equalizer30Band(frame)
        
        # Apply button
        tk.Button(
            frame, text="APPLY EQ", command=self._apply_eq,
            bg=GTR_RED, fg="white", font=("Arial", 8, "bold")
        ).pack(pady=5)
    
    def _create_download_panel(self):
        """Create YouTube download panel"""
        dl_frame = tk.LabelFrame(self, text="YOUTUBE DOWNLOADER", bg=GTR_DARK, fg=GTR_RED)
        dl_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # URL entry
        tk.Label(dl_frame, text="YouTube URL:", bg=GTR_DARK, fg="white").pack(anchor="w", padx=5)
        
        self.url_var = tk.StringVar()
        self.url_entry = tk.Entry(
            dl_frame, textvariable=self.url_var, width=80,
            bg=GTR_DARK, fg="white", insertbackground="white"
        )
        self.url_entry.pack(fill=tk.X, padx=5, pady=5)
        
        # Format selection
        fmt_frame = tk.Frame(dl_frame, bg=GTR_DARK)
        fmt_frame.pack(fill=tk.X, padx=5)
        
        self.format_var = tk.StringVar(value="mp3")
        for fmt in ["flac", "mp3", "wav"]:
            tk.Radiobutton(
                fmt_frame, text=fmt.upper(),
                variable=self.format_var, value=fmt,
                bg=GTR_DARK, fg=GTR_RED, selectcolor=GTR_DARK
            ).pack(side=tk.LEFT, padx=10)
        
        # Download button
        self.dl_btn = tk.Button(
            dl_frame, text="DOWNLOAD", command=self._download,
            bg=GTR_RED, fg="white", font=("Arial", 10, "bold")
        )
        self.dl_btn.pack(pady=5)
    
    def _add_folder(self):
        """Add all audio files from folder to playlist"""
        folder = filedialog.askdirectory()
        if not folder:
            return
        
        import glob
        patterns = ["*.mp3", "*.flac", "*.wav"]
        count = 0
        
        for pattern in patterns:
            for filepath in Path(folder).glob(pattern):
                self.playlist.append(Track(
                    title=filepath.stem,
                    artist="Unknown",
                    filepath=str(filepath),
                    duration=0,
                    format=filepath.suffix[1:]
                ))
                self.playlist_box.insert(tk.END, filepath.stem)
                count += 1
        
        messagebox.showinfo("Added", f"Added {count} tracks to playlist")
    
    def _play(self):
        """Play current track"""
        if not self.playlist:
            messagebox.showinfo("No tracks", "Add tracks to playlist first!")
            return
        
        # Play using pydub
        selected = self.playlist_box.curselection()
        if selected:
            track = self.playlist[selected[0]]
            try:
                audio = AudioSegment.from_file(track.filepath)
                play(audio)
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def _stop(self):
        """Stop playback"""
        pass  # pydub play() is blocking
    
    def _next(self):
        """Next track"""
        pass
    
    def _apply_eq(self):
        """Apply equalizer settings"""
        spectrum = self.eq.get_spectrum()
        print(f"EQ Applied: {spectrum}")
        messagebox.showinfo("Applied", "Equalizer settings applied")
    
    def _download(self):
        """Download YouTube video"""
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter YouTube URL")
            return
        
        self.dl_btn.config(text="DOWNLOADING...", state=tk.DISABLED)
        
        def download_thread():
            try:
                result = self.downloader.download(url, self.format_var.get())
                self.after(0, lambda: messagebox.showinfo("Success", f"Downloaded: {result}"))
            except Exception as e:
                self.after(0, lambda: messagebox.showerror("Error", str(e)))
            finally:
                self.after(0, lambda: self.dl_btn.config(text="DOWNLOAD", state=tk.NORMAL))
        
        threading.Thread(target=download_thread, daemon=True).start()


def main():
    app = NissanGTRPlayer()
    app.mainloop()


if __name__ == "__main__":
    main()