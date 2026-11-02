# service_manager.py
"""
Service manager for running the local LLM translation and TTS engine in background

This module provides functionality to start, stop, and check the status of the
translation and text-to-speech service as a background process.
"""

import subprocess
import sys
import os
import time

class ServiceManager:
    """
    Manages the lifecycle of the translation and TTS service as a background process.

    This class handles starting, stopping, and checking the status of the main
    application process that performs translation and speech synthesis tasks.

    Attributes:
        service_process (subprocess.Popen): Reference to the running service process
    """

    def __init__(self):
        """Initialize the ServiceManager with no active process."""
        self.service_process = None
        
    def start_service(self):
        """
        Start the main application as a background service.

        This method launches the main application script as a separate process,
        allowing it to run in the background while this manager continues.

        Returns:
            bool: True if service started successfully, False otherwise
        """
        try:
            print("Starting Local LLM Translation & TTS Service...")

            # Start the main application in background using subprocess
            self.service_process = subprocess.Popen([
                sys.executable, "main_app.py"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print("Service started successfully")
            print("Process ID:", self.service_process.pid)
                return True
            except Exception as e:
            print(f"Failed to start service: {e}")
                return False

    def stop_service(self):
        """
        Stop the background service gracefully.

        This method attempts to terminate the running service process. If the
        process doesn't respond to termination, it will be forcefully killed.
        Returns:
            bool: True if service stopped successfully, False otherwise
        """
        if self.service_process:
            try:
                # Attempt graceful termination first
                self.service_process.terminate()
                self.service_process.wait(timeout=5)
                print("Service stopped successfully")
                return True
            except subprocess.TimeoutExpired:
                # Force kill if termination times out
                self.service_process.kill()
                print("Service killed after timeout")
                return True
            except Exception as e:
                print(f"Error stopping service: {e}")
                return False
        else:
            print("No service running")
            return False

    def is_service_running(self):
        """
        Check if the service process is currently running.

        Returns:
            bool: True if service is running, False otherwise
        """
        if self.service_process:
            # poll() returns None if process is still running, or exit code if not
            return self.service_process.poll() is None
        return False

def main():
    """
    Main entry point for the service manager.

    Handles command-line arguments to control the service lifecycle:
    - start: Launches the service
    - stop: Stops the service
    - status: Checks if service is running
    """
    manager = ServiceManager()

    # Check if command-line arguments were provided
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()

        if command == "start":
            # Start the service
            manager.start_service()
        elif command == "stop":
            # Stop the service
            manager.stop_service()
        elif command == "status":
            # Check service status
            print(f"Service running: {manager.is_service_running()}")
    else:
            # Invalid command provided
        print("Usage: python service_manager.py [start|stop|status]")
    else:
        # No arguments provided, show usage instructions
        print("Usage: python service_manager.py [start|stop|status]")

if __name__ == "__main__":
    main()