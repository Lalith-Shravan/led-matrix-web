from os.path import dirname, join
from os import environ

from app import createApp, startProcessQueueService
from app.display.led_display import LEDDisplay
from app.utils.drop_privileges import drop_privileges

PROJ_PATH = dirname(__file__)
APP_PATH = join(PROJ_PATH, "app")
UPLOAD_PATH = join(APP_PATH, "web", "static", "uploads")
DEFAULT_FONT_PATH = join(PROJ_PATH, "fonts", "9x18.bdf")
DEFAULT_BOLD_FONT_PATH = join(PROJ_PATH, "fonts", "9x18B.bdf")

# Only start the queue *after* the reloader has launched the actual server
if environ.get('WERKZEUG_RUN_MAIN') == 'true':
    
    display = LEDDisplay(led_slowdown_gpio=4,
                        led_gpio_mapping="adafruit-hat",
                        limit_refresh_rate_hz=120,
                        font_path=DEFAULT_FONT_PATH,
                        bold_font_path=DEFAULT_BOLD_FONT_PATH,
                        led_chain=2)
    
    # Manually drop privileges
    drop_privileges("pi") # Change this to your own user

    queue = startProcessQueueService(display)


else:
    queue = None
    display = None

app = createApp(queue, display, UPLOAD_PATH)

if __name__ == "__main__":
    app.run("0.0.0.0", debug=True)