# Local LLM Translation & TTS Engine

A powerful application that combines local language models with text-to-speech capabilities for real-time translation and speech synthesis.

## Features

- **Local LLM Translation**: Uses Ollama with Qwen3.6 27B model for high-quality translations
- **Text-to-Speech**: Integrates with Microsoft's Edge-TTS for natural voice synthesis
- **Multi-language Support**: Translate to various languages (default is Polish)
- **AutoHotkey Integration**: Can be triggered from AutoHotkey scripts
- **Background Service**: Run as a persistent background process

## Architecture

The application consists of three main components:

1. **TranslationEngine**: Handles communication with Ollama service for text translation
2. **EdgeTTS**: Manages text-to-speech functionality using Microsoft's Edge-TTS
3. **BackgroundService**: Coordinates the entire workflow between translation and speech synthesis

## Prerequisites

Before running this application, you need:

1. **Ollama** - Local LLM runtime
   - Download from: https://ollama.com/download
   - Pull the required model: `ollama pull qwen3.6:27b`

2. **Python 3.7+** with required packages:
   ```bash
   pip install requests edge-tts
   ```

## Setup Instructions

### 1. Install Ollama
- Download and install Ollama from https://ollama.com/download
- Pull the Qwen3.6 27B model: `ollama pull qwen3.6:27b`

### 2. Install Python Dependencies
```bash
pip install requests edge-tts
```

### 3. Run the Application
```bash
python main_app.py
```

## Usage

### Command Line Interface
The application provides a command-line interface for immediate use:

```python
# Basic usage - translates to Polish (default)
service.translate_and_speak("Hello world")

# Translate to French
service.translate_and_speak("Hello world", "fr")

# Translate to German  
service.translate_and_speak("Hello world", "de")
```

### AutoHotkey Integration
The application includes AutoHotkey integration capabilities. You can trigger translations from AutoHotkey scripts by calling:

```autohotkey
; Example AutoHotkey script
Run, python main_app.py
Sleep, 1000

; Trigger translation with AutoHotkey
Run, python -c "from service_manager import AutoHotkeyIntegration; AutoHotkeyIntegration.run_translation('Hello world', 'pl')"
```

## Service Management

Use the service manager to control the application as a background process:

```bash
# Start the service
python service_manager.py start

# Check status
python service_manager.py status

# Stop the service  
python service_manager.py stop
```

## Project Structure

```
.
├── main_app.py          # Main application with translation and TTS functionality
├── service_manager.py   # Service management for background operation
└── README.md            # This documentation file
```

## Configuration

### Default Settings
- **Translation Model**: Qwen3.6 27B (requires local installation)
- **Default Language**: Polish (pl-PL-ZofiaNeural voice)
- **Ollama API Port**: localhost:11434

### Customization Options
You can modify the following in `main_app.py`:
- Change the default translation model by modifying `model_name`
- Add support for additional voices by updating `default_voice`
- Adjust the target language in `translate_and_speak()` method calls

## Error Handling

The application includes comprehensive error handling:

1. **Ollama Connection**: Checks if Ollama service is running and has the required model
2. **Edge-TTS Initialization**: Automatically installs Edge-TTS if missing
3. **Translation Failures**: Gracefully handles translation errors
4. **Speech Synthesis**: Provides fallback behavior when TTS fails

## Troubleshooting

### Common Issues

1. **Ollama not running**: Ensure Ollama is installed and started before running the application
2. **Model not found**: Run `ollama pull qwen3.6:27b` to download the required model
3. **Edge-TTS installation**: The application will automatically install Edge-TTS if missing
4. **Port conflicts**: Ensure port 11434 is available for Ollama

### Debugging

Enable verbose logging by adding print statements or using Python's logging module for detailed operation information.

## License

This project is created for personal and educational purposes. Please ensure you comply with the licenses of all third-party components used (Ollama, Edge-TTS, etc.).

## Author

Local LLM Translation & TTS Engine