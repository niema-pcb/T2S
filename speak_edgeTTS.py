import asyncio
import edge_tts
import pygame  

async def main():
    pygame.mixer.init()

    while True:
        text = input("Say something (or type 'quit'): ")
        if text.lower() == "quit":
            break
        
        communicate = edge_tts.Communicate(text, "pl-PL-ZofiaNeural")
        await communicate.save("output.mp3")
    
        pygame.mixer.music.load("output.mp3")
        pygame.mixer.music.play()
    
        while pygame.mixer.music.get_busy():
            await asyncio.sleep(0.1)    
        
        
        pygame.mixer.music.unload()  # frees output.mp3 for the next round
    
    pygame.mixer.quit()

asyncio.run(main())