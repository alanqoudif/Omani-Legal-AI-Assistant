import os
import numpy as np
import whisper
import io
import tempfile
from pydub import AudioSegment
import streamlit as st

class SpeechToText:
    """Class to handle speech-to-text conversion"""
    
    def __init__(self, language="en"):
        """
        Initialize the speech-to-text system.
        
        Args:
            language: Language code ("en" for English, "ar" for Arabic)
        """
        self.language = language
        self.model = None
    
    def load_model(self, model_size="base"):
        """
        Load the Whisper model.
        
        Args:
            model_size: Size of the Whisper model to use (tiny, base, small, medium, large)
        """
        try:
            # Check if model is already loaded
            if self.model is None:
                # Load model with progress indicator in Streamlit
                with st.spinner(f"Loading speech recognition model ({model_size})..."):
                    self.model = whisper.load_model(model_size)
                st.success("Speech recognition model loaded!")
            return True
        except Exception as e:
            st.error(f"Error loading Whisper model: {str(e)}")
            return False
    
    def transcribe_audio(self, audio_data, detect_language=True):
        """
        Transcribe audio to text.
        
        Args:
            audio_data: Audio data bytes
            detect_language: Whether to automatically detect the language
            
        Returns:
            Transcribed text
        """
        try:
            # Make sure model is loaded
            if self.model is None:
                if not self.load_model():
                    return "Error: Could not load speech recognition model."
            
            # Save audio bytes to a temporary file
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
                temp_audio.write(audio_data)
                temp_audio_path = temp_audio.name
            
            # Set options based on language
            options = {}
            if not detect_language:
                options["language"] = "en" if self.language == "English" else "ar"
            
            # Transcribe the audio
            result = self.model.transcribe(temp_audio_path, **options)
            
            # Clean up temporary file
            os.unlink(temp_audio_path)
            
            return result["text"]
        
        except Exception as e:
            return f"Error transcribing audio: {str(e)}"

def preprocess_audio(audio_bytes):
    """
    Preprocess audio for better recognition quality.
    
    Args:
        audio_bytes: Raw audio bytes
        
    Returns:
        Processed audio bytes
    """
    try:
        # Convert audio bytes to AudioSegment
        audio = AudioSegment.from_file(io.BytesIO(audio_bytes))
        
        # Normalize audio (adjust volume to a standard level)
        normalized_audio = audio.normalize()
        
        # Convert to mono if stereo
        if normalized_audio.channels > 1:
            normalized_audio = normalized_audio.set_channels(1)
        
        # Set sample rate to 16kHz (optimal for many speech recognition models)
        normalized_audio = normalized_audio.set_frame_rate(16000)
        
        # Export processed audio to bytes
        processed_bytes = io.BytesIO()
        normalized_audio.export(processed_bytes, format="wav")
        
        return processed_bytes.getvalue()
    
    except Exception as e:
        print(f"Error preprocessing audio: {e}")
        return audio_bytes  # Return original bytes if processing fails
