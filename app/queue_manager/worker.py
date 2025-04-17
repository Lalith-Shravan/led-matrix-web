from queue import *
import os
from threading import Thread

from ..display.led_display import LEDDisplay
from ..utils import getFileExtension

from app.display.rich_text import RichText


def startProcessQueueService():
    queue = Queue()

    def processQueueService():
        # TODO: Make options customizable
        display = LEDDisplay(led_slowdown_gpio=4, led_gpio_mapping="adafruit-hat",limit_refresh_rate_hz=120)

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