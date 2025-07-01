from queue import *
import os
from threading import Thread

from ..display.led_display import LEDDisplay
from ..utils import getFileExtension

from app.display.rich_text import RichText


def startProcessQueueService(display: LEDDisplay):
    queue = Queue()

    def processQueueService():

        while True:
            try:
                message = queue.get(timeout=1)

                if isinstance(message, list):
                    display.drawText(message)

                elif isinstance(message, str):
                    
                    if getFileExtension(message) == "gif":
                        display.displayAnimation(message)
                    else:
                        display.displayImage(message)

                    os.remove(message)
            
            except Empty:
                continue
            
            except Exception as e:
                print(f"Unexpected error: {e}")

    Thread(target=processQueueService, daemon=True).start()

    return queue