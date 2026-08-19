"""
Nissan GTR Music Player - Audio Components
30-Band parametric equalizer with preset management
"""
import os
import sys
import tempfile
import threading
import json
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, List, Callable, Dict, Tuple
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import numpy as np
from pydub import AudioSegment
from pydub.playback import play

try:
    from pytube import YouTube
except ImportError:
    YouTube = None

# Nissan GTR Red Theme Colors
GTR_RED = "#D40000"
GTR_DARK = "#1A0000"
GTR_BRIGHT_RED = "#FF3B30"
GTR_GRAY = "#333333"
GTR_LIGHT = "#FA8072"


@dataclass
class Track:
    """Represents a music track"""
    title: str
    artist: str
    filepath: str
    duration: float
    format: str


class EqualizerPresetManager:
    """Manage equalizer presets"""
    
    DEFAULT_PRESETS = {
        "Flat": [0.0] * 30,
        "Bass Boost": [3, 2, 2, 1, 1, 0, 0, -1, -1, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 1, 1, 2, 2, 3, 2, 1, 0, 0, 0, 0],
        "Treble Enhanced": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 1, 2, 3, 3, 4, 3, 3, 2, 2, 1, 1, 0, 0],
        "Rock Preset": [2, 2, 3, 3, 3, 2, 1, 0, -1, -1, 0, 0, 1, 2, 3,
                        4, 4, 4, 3, 2, 1, 0, -1, -1, -2, -1, 0, 0, 0, 0],
        "Pop Preset": [0, 1, 1, 1, 2, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 1, 2, 3, 3, 2, 1, 0, 0, 0, 0, 0, 0],
        "Classical": [1, 0, -1, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, -1, 0, 0],
        "Jazz": [1, 2, 2, 2, 1, 0, -1, -1, -1, -2, -2, -2, -1, 0, 1,
                 2, 3, 4, 4, 3, 2, 1, 0, -1, 0, 1, 2, 3, 2, 1],
    }
    
    def __init__(self, manager):
        self.manager = manager
        self.presets_file = "equalizer_presets.json"
    
    def load_presets(self) -> Dict[str, List[float]]:
        """Load presets from file or return defaults"""
        try:
            with open(self.presets_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return self.DEFAULT_PRESETS.copy()
    
    def save_preset(self, name: str, values: List[float]):
        """Save a preset"""
        presets = self.load_presets()
        presets[name] = values
        with open(self.presets_file, 'w') as f:
            json.dump(presets, f, indent=2)
    
    def apply_preset(self, name: str):
        """Apply preset to equalizer"""
        presets = self.load_presets()
        if name in presets:
            self.manager.set_from_csv(presets[name])


class Equalizer30Band:
    """30-band parametric equalizer with visualization"""
    
    FREQUENCIES = [
        20, 25, 31.5, 40, 50, 63, 80, 100,
        125, 160, 200, 250, 315, 400, 500, 630,
        800, 1000, 1250, 1600, 2000, 2500, 3150, 4000,
        5000, 6300, 8000, 10000, 12500, 16000
    ]
    
    def __init__(self, parent, style_manager=None):
        self.parent = parent
        self.style = style_manager
        self.sliders: List[tk.Scale] = []
        self.values: List[float] = [0.0] * 30
        self.visualizer = None
        self.preset_manager = EqualizerPresetManager(self)
        
        self._create_eq_section()
    
    def _create_eq_section(self):
        """Create complete equalizer UI"""
        
        # Title
        tk.Label(
            self.parent, text="30-BAND EQUALIZER",
            font=("Arial", 12, "bold"), fg=GTR_RED, bg=GTR_DARK
        ).pack(pady=5)
        
        # Preset selector
        preset_frame = tk.Frame(self.parent, bg=GTR_DARK)
        preset_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(
            preset_frame, text="Preset:",
            font=("Consolas", 10), fg="white", bg=GTR_DARK
        ).pack(side=tk.LEFT)
        
        self.preset_var = tk.StringVar(value="Flat")
        self.preset_combo = ttk.Combobox(
            preset_frame,
            textvariable=self.preset_var,
            values=["Flat", "Bass Boost", "Treble Enhanced",
                   "Rock Preset", "Pop Preset", "Classical", "Jazz", "Custom"],
            state="readonly",
            width=15
        )
        self.preset_combo.pack(side=tk.LEFT, padx=5)
        self.preset_combo.set("Flat")
        self.preset_combo.pack(side=tk.LEFT, padx=5)
        self.preset_combo.bind("<<ComboboxSelected>>", self._on_preset_select)
        
        tk.Button(
            preset_frame, text="APPLY PRESET",
            command=self._apply_preset,
            bg=GTR_RED, fg="white", font=("Arial", 8, "bold")
        ).pack(side=tk.LEFT, padx=5)
        
        # Frequency labels
        labels_frame = tk.Frame(self.parent, bg=GTR_DARK)
        labels_frame.pack(fill=tk.X, padx=10, pady=(0, 5))
        
        for i, freq in enumerate(self.FREQUENCIES[:15]):
            label = tk.Label(labels_frame, text=f"{freq}Hz",
                           font=("Consolas", 6), fg="#AAA", bg=GTR_DARK)
            label.grid(row=0, column=i, padx=1)
        
        for i, freq in enumerate(self.FREQUENCIES[15:]):
            label = tk.Label(labels_frame, text=f"{freq}Hz",
                           font=("Consolas", 6), fg="#AAA", bg=GTR_DARK)
            label.grid(row=1, column=i, padx=1)
        
        # Sliders (30 total - 15 per row)
        sliders_frame = tk.Frame(self.parent, bg=GTR_DARK)
        sliders_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Top row sliders (bands 0-14)
        for i in range(15):
            slider = tk.Scale(sliders_frame, from_=-12, to=+12,
                             orient=tk.HORIZONTAL, length=80,
                             bg=GTR_DARK, fg=GTR_RED,
                             highlightthickness=1, highlightbackground=GTR_RED,
                             troughcolor=GTR_GRAY, sliderlength=12)
            slider.set(0)
            slider.grid(row=0, column=i, padx=1, sticky="n")
            slider.bind("<ButtonRelease>", self._on_slider_move)
            self.sliders.append(slider)
        
        # Bottom row sliders (bands 15-29)
        for i in range(15):
            slider = tk.Scale(sliders_frame, from_=-12, to=+12,
                             orient=tk.HORIZONTAL, length=80,
                             bg=GTR_DARK, fg=GTR_RED,
                             highlightthickness=1, highlightbackground=GTR_RED,
                             troughcolor=GTR_GRAY, sliderlength=12)
            slider.set(0)
            slider.grid(row=1, column=i, padx=1, sticky="n")
            slider.bind("<ButtonRelease>", self._on_slider_move)
            self.sliders.append(slider)
    
    def _on_preset_select(self, event):
        """Handle preset selection"""
        preset = self.preset_var.get()
        if preset == "Custom":
            return
        self.preset_manager.apply_preset(preset)
        self._update_visualizer()
    
    def _apply_preset(self):
        """Apply selected preset"""
        preset = self.preset_var.get()
        self.preset_manager.apply_preset(preset)
        self._update_visualizer()
    
    def _save_preset_dialog(self):
        """Dialog to save current settings as preset"""
        name = tk.simpledialog.askstring("Save Preset", "Enter preset name:")
        if name:
            self.preset_manager.save_preset(name, self.values.copy())
    
    def _on_slider_move(self, event):
        """Update values when slider moves"""
        for i, s in enumerate(self.sliders):
            self.values[i] = float(s.get())
        self._update_visualizer()
    
    def _update_visualizer(self):
        """Update visual representation (placeholder)"""
        pass
    
    def get_spectrum(self) -> np.ndarray:
        """Get current equalizer settings as numpy array"""
        return np.array(self.values)
    
    def set_from_csv(self, values: List[float]):
        """Set all sliders from a CSV value list"""
        for i, val in enumerate(values[:30]):
            if i < len(self.sliders):
                self.sliders[i].set(val)
                self.values[i] = float(val)
        self._update_visualizer()