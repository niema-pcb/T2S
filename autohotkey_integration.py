# autohotkey_integration.py
"""
AutoHotkey integration script for context menu translation

This file provides functionality to generate an AutoHotkey script that enables
context menu integration for the Local LLM Translation & TTS Engine. The generated
script adds a "Translate with Local LLM" option to the system tray context menu
that allows users to quickly translate selected text using the local AI model.

The script automatically:
1. Creates a context menu item in the system tray
2. Captures selected text from clipboard
3. Calls the translation service with the selected text
4. Starts the main application in background
"""

import subprocess
import sys
import os

def create_autohotkey_script():
    """
    Create an AutoHotkey script for context menu integration.
    
    This function generates a complete AutoHotkey script that:
    - Adds a "Translate with Local LLM" item to the system tray context menu
    - Captures selected text from clipboard when invoked
    - Calls the Python translation service with the selected text
    - Starts the main application in background

    The generated script will be saved as 'translate_with_llm.ahk'
    """

    # AutoHotkey script content with detailed comments
    ahk_content = """
; Local LLM Translation and TTS Context Menu
#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.

; Create context menu item
Menu, Tray, Add, Translate with Local LLM, TranslateText
Menu, Tray, Default, Translate with Local LLM
Menu, Tray, Tip, Local LLM Translation Service

; Main translation function triggered by context menu
TranslateText:
    ; Save the current clipboard content to restore it later
    ClipSaved := ClipboardAll
    Clipboard := ""

    ; Copy selected text (assumes text is already selected)
    Send, ^c  ; Copy selected text using Ctrl+C

    ; Small delay to ensure copy operation completes
    Sleep, 100

    ; Check if clipboard has content before proceeding
    if (Clipboard != "") {
        ; Call the Python translation service with the copied text
        ; The script passes the text and target language (pl for Polish)
        Run, python "%A_ScriptDir%\main_app.py" translate "%Clipboard%" pl

        ; Optional: Speak the translated text
        ; Run, python "%A_ScriptDir%\main_app.py" speak "%Clipboard%" pl
    }

    ; Restore original clipboard content
    Clipboard := ClipSaved
return

; Handle tray icon clicks (exit application)
TrayClick:
    ExitApp
return

; Start the Python service in background when script is launched
#SingleInstance Force
Run, python "%A_ScriptDir%\main_app.py"
"""

    # Write the AutoHotkey script to file
    with open("translate_with_llm.ahk", "w") as f:
        f.write(ahk_content)
    
    print("AutoHotkey script created: translate_with_llm.ahk")
    print("Run this script to enable context menu integration")
    print("You'll also need to install AutoHotkey from https://www.autohotkey.com/")

if __name__ == "__main__":
    """
    Main entry point for the AutoHotkey integration script generator.

    When executed, this script will generate a complete AutoHotkey script that
    provides context menu integration for the translation service.
    """
    create_autohotkey_script()