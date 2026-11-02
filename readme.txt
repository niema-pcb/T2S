# Local LLM Translation & TTS Engine

A lightweight local translation and text-to-speech engine using Ollama with Qwen3.6 27B model and Edge-TTS for Polish language support.

## Features

- **Translation**: Uses Ollama with Qwen3.6 27B model for high-quality translations
- **Text-to-Speech**: Uses Edge-TTS with Polish voice (ZofiaNeural) as default
- **Background Service**: Runs continuously in the background
- **Context Menu Integration**: Works with AutoHotkey for easy access from context menu
- **Cross-platform**: Can be extended to work on different platforms

## Requirements

### System Requirements:
1. Python 3.7+
2. Ollama (https://ollama.com/download)
3. Qwen3.6 27B model installed via Ollama

### Installation:

1. Install required packages:
```bash
pip install torch transformers accelerate numpy edge-tts requests pystray PyQt5
```

2. Install Ollama from https://ollama.com/download and pull the model:
```bash
ollama pull qwen3.6:27b
```

## Usage

### 1. Run the main application:
```bash
python main_app.py
```

### 2. For AutoHotkey integration:
```bash
python autohotkey_integration.py
```

This creates `translate_with_llm.ahk` which you can run with AutoHotkey to enable context menu translation.

### 3. Service management:
```bash
python service_manager.py start    # Start service
python service_manager.py stop     # Stop service  
python service_manager.py status   # Check status
```

## Functionality

The system provides:
- **Continuous background operation** with Ollama and Edge-TTS
- **Polish language default** for all translations and speech output
- **Context menu integration** via AutoHotkey
- **Simple API** for external tools to access translation and TTS capabilities

## Configuration

The service can be configured through:
- Default Polish language (pl) for translations
- Edge-TTS voice settings in `EdgeTTS` class
- Ollama model selection in `TranslationEngine`

## AutoHotkey Integration

1. Run `autohotkey_integration.py` to generate the AutoHotkey script
2. Install AutoHotkey from https://www.autohotkey.com/
3. Run the generated `.ahk` file to enable context menu integration
4. Right-click on text in any application to translate and speak it aloud

## License

MIT License