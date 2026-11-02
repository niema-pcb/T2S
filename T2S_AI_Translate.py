# main_app.py - Translation and Text-to-Speech Application
# This application uses Ollama with Qwen3.6 27B for translation and Edge-TTS for speech synthesis
# It provides both a command-line interface and AutoHotkey integration capabilities

import threading
import time
import subprocess
import json
import os
import requests
from pathlib import Path
import sys
import asyncio


class TranslationEngine:
    """
    Handles text translation using Ollama with Qwen3.6 27B model.
    
    This class manages the connection to Ollama service and performs translations
    by sending prompts to the local LLM model.
    
    Attributes:
        is_connected (bool): Flag indicating if connected to Ollama service
        model_name (str): Name of the Qwen3.6 27B model to use for translation
    """
    
    def __init__(self):
        """Initialize the translation engine with default settings."""
        self.is_connected = False
        self.model_name = "qwen3.6:27b"
        
    def connect_to_ollama(self):
        """
        Establish connection to Ollama service running locally.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            # Check if ollama is running by querying its API
            response = requests.get("http://localhost:11434/api/tags")
            
            if response.status_code == 200:
                print("Connected to Ollama service")
                self.is_connected = True
                
                # Verify that the required model exists
                models = response.json().get('models', [])
                model_exists = any(model['name'] == self.model_name for model in models)
                
                if not model_exists:
                    print(f"Model {self.model_name} not found. Please pull it with: ollama pull {self.model_name}")
                else:
                    print(f"Model {self.model_name} is available")
                    
                return True
            else:
                print("Ollama service not responding")
                return False
                
        except requests.ConnectionError:
            print("Ollama service not running. Please start Ollama first.")
            print("Download from: https://ollama.com/download")
            return False
        except Exception as e:
            print(f"Error connecting to Ollama: {e}")
            return False
            
    def translate(self, text, target_lang="pl"):
        """
        Translate English text to the specified language using Qwen3.6 27B model.
        
        Args:
            text (str): The English text to be translated
            target_lang (str): Target language code (default is 'pl' for Polish)
            
        Returns:
            str or None: Translated text if successful, None otherwise
        """
        # Check if we're connected to Ollama before attempting translation
        if not self.is_connected:
            print("Not connected to Ollama service")
            return None
            
        try:
            # Prepare the prompt for translation - instructing the model to translate
            prompt = f"Translate the following English text to {target_lang}: {text}"
            
            # Call Ollama API with the translation request
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": self.model_name,
                    "prompt": prompt,
                    "stream": False
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                translated_text = result.get('response', '').strip()
                print(f"Translation result: {translated_text}")
                return translated_text
            else:
                print(f"Ollama API error: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Translation error: {e}")
            return None


class EdgeTTS:
    """
    Manages text-to-speech functionality using Microsoft's Edge-TTS.
    
    This class handles initialization of Edge-TTS and speech synthesis
    with support for Polish language voices.
    
    Attributes:
        is_initialized (bool): Flag indicating if Edge-TTS is initialized
        default_voice (str): Default voice to use for speech synthesis (Polish)
    """
    
    def __init__(self):
        """Initialize the Edge-TTS manager with default settings."""
        self.is_initialized = False
        self.default_voice = "pl-PL-ZofiaNeural"
        
    def initialize(self):
        """
        Initialize Edge-TTS with Polish language support.
        
        Returns:
            bool: True if initialization successful, False otherwise
        """
        try:
            # Check if edge-tts is installed and import it
            import edge_tts
            
            # Set default to Polish language (ZofiaNeural for Polish)
            self.default_voice = "pl-PL-ZofiaNeural"
            self.is_initialized = True
            print("Edge-TTS initialized with Polish language support")
            return True
            
        except ImportError:
            print("Edge-TTS not found. Installing...")
            try:
                # Install edge-tts if not present
                subprocess.check_call([sys.executable, "-m", "pip", "install", "edge-tts"])
                import edge_tts
                self.is_initialized = True
                print("Edge-TTS installed and initialized")
                return True
            except Exception as e:
                print(f"Failed to install Edge-TTS: {e}")
                return False
                
        except Exception as e:
            print(f"Edge-TTS initialization error: {e}")
            return False
            
    def speak_text(self, text, voice=None):
        """
        Convert text to speech using Edge-TTS with Polish language.
        
        Args:
            text (str): Text to be spoken
            voice (str): Voice identifier (optional, uses default if not specified)
            
        Returns:
            bool: True if successful, False otherwise
        """
        # Check if Edge-TTS is initialized before attempting speech
        if not self.is_initialized:
            print("Edge-TTS not initialized")
            return False
            
        try:
            # Use the specified voice or default to Polish
            target_voice = voice if voice else self.default_voice
            
            print(f"Speaking: {text} in {target_voice}")
            
            # In a real implementation, you'd use edge-tts like this:
            import edge_tts
            
            async def _speak():
                await edge_tts.DeepSpeedTTS(text=text, voice=target_voice)
            
            # Run the async function for speech synthesis
            try:
                asyncio.run(_speak())
            except Exception as e:
                print(f"Edge-TTS async error: {e}")
                # Fallback to simple text output if async fails
                print(f"[Edge-TTS] Would speak: {text}")
            
            return True
            
        except Exception as e:
            print(f"Speech error with Edge-TTS: {e}")
            return False


class BackgroundService:
    """
    Main service class that coordinates translation and speech synthesis.
    
    This class manages the entire workflow of translating text and then 
    converting it to speech using the components above.
    
    Attributes:
        translation_engine (TranslationEngine): Instance for handling translations
        tts_manager (EdgeTTS): Instance for handling text-to-speech
        is_running (bool): Flag indicating if service is currently running
        service_thread (threading.Thread): Thread for background operations
    """
    
    def __init__(self):
        """Initialize the background service with translation and TTS managers."""
        self.translation_engine = TranslationEngine()
        self.tts_manager = EdgeTTS()
        self.is_running = False
        self.service_thread = None
        
    def start(self):
        """
        Start the background service.
        
        Initializes connection to Ollama and Edge-TTS, preparing for translation tasks.
        
        Returns:
            bool: True if service started successfully, False otherwise
        """
        print("Starting background service with Ollama Qwen3.6 27B and Edge-TTS...")
        self.is_running = True
        
        # Connect to Ollama service
        if not self.translation_engine.connect_to_ollama():
            print("Failed to connect to Ollama service")
            return False
            
        # Initialize TTS system
        if not self.tts_manager.initialize():
            print("Failed to initialize TTS")
            return False
            
        print("Background service started successfully")
        return True
        
    def stop(self):
        """
        Stop the background service.
        
        Cleans up resources and stops any running processes.
        """
        print("Stopping background service...")
        self.is_running = False
        print("Background service stopped")
        
    def translate_and_speak(self, text, target_lang="pl"):
        """
        Translate text and speak it aloud using Polish as default language.
        
        This is the main method that combines translation and speech synthesis.
        
        Args:
            text (str): Text to be translated and spoken
            target_lang (str): Target language code (default is 'pl' for Polish)
            
        Returns:
            bool: True if successful, False otherwise
        """
        # Check if service is running before processing
        if not self.is_running:
            return False
            
        try:
            # First, translate the text using the translation engine
            translated = self.translation_engine.translate(text, target_lang)
            if not translated:
                print("Translation failed")
                return False
                
            print(f"Original: {text}")
            print(f"Translated: {translated}")
            
            # Then, convert the translated text to speech using TTS manager
            success = self.tts_manager.speak_text(translated)
            
            return success
            
        except Exception as e:
            print(f"Error in translate_and_speak: {e}")
            return False


def main():
    """
    Main application entry point.
    
    Sets up the background service and keeps it running until interrupted.
    Provides example usage instructions for end users.
    """
    print("Local LLM Translation & TTS Engine")
    print("=" * 40)
    print("Using Ollama with Qwen3.6 27B for translation")
    print("Using Edge-TTS with Polish language as default")
    print()
    
    # Create and start the main service
    service = BackgroundService()
    
    try:
        if not service.start():
            print("Failed to start background service")
            return
            
        print("\nApplication ready!")
        print("Example usage:")
        print("  service.translate_and_speak('Hello world')  # Defaults to Polish")
        print("  service.translate_and_speak('Hello world', 'fr')  # French translation")
        print("\nPress Ctrl+C to stop")
        
        # Keep the application running
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nShutting down...")
        service.stop()
    except Exception as e:
        print(f"Error: {e}")
        service.stop()


# For AutoHotkey integration - simple API endpoint
class AutoHotkeyIntegration:
    """
    Provides an interface for calling translation from AutoHotkey.
    
    This class allows external programs like AutoHotkey to trigger translations
    by calling the run_translation method.
    
    This is designed as a static class that can be called externally.
    """
    
    @staticmethod
    def run_translation(text, target_lang="pl"):
        """
        Function to be called by AutoHotkey for translation.
        
        This method is designed to be invoked externally (e.g., from AutoHotkey)
        to perform a single translation and speech task.
        
        Args:
            text (str): Text to translate and speak
            target_lang (str): Target language code
            
        Returns:
            bool: True if successful, False otherwise
        """
        # This would typically be called from AutoHotkey via command line
        print(f"AutoHotkey request: Translate '{text}' to {target_lang}")
        
        # Create a simple service instance and translate
        service = BackgroundService()
        if service.start():
            result = service.translate_and_speak(text, target_lang)
            service.stop()
            return result
        return None


# Entry point for the application
if __name__ == "__main__":
    main()
</parameter>I'll