import time
from typing import Optional

from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics

class LEDDisplay:
    def __init__(self,
                 led_rows=32,
                 led_cols=64,
                 led_chain=1,
                 led_parallel=1,
                 led_pwm_bits=11,
                 led_brightness=100,
                 led_gpio_mapping="regular",
                 led_scan_mode=1,
                 led_pwm_lsb_nanoseconds=130,
                 led_show_refresh=True,
                 led_slowdown_gpio=1,
                 led_no_hardware_pulse=False,
                 led_rgb_sequence="RGB",
                 led_pixel_mapper="",
                 led_row_addr_type=0,
                 led_multiplexing=0,
                 led_panel_type="",
                 drop_privileges=False,
                 limit_refresh_rate_hz = None):
        
        options = RGBMatrixOptions()

        options.hardware_mapping = led_gpio_mapping
        options.rows = led_rows
        options.cols = led_cols
        options.chain_length = led_chain
        options.parallel = led_parallel
        options.row_address_type = led_row_addr_type
        options.multiplexing = led_multiplexing
        options.pwm_bits = led_pwm_bits
        options.brightness = led_brightness
        options.pwm_lsb_nanoseconds = led_pwm_lsb_nanoseconds
        options.led_rgb_sequence = led_rgb_sequence
        options.pixel_mapper_config = led_pixel_mapper
        options.panel_type = led_panel_type
        options.show_refresh_rate = 1 if led_show_refresh else 0
        options.gpio_slowdown = led_slowdown_gpio
        options.disable_hardware_pulsing = led_no_hardware_pulse
        options.drop_privileges=not drop_privileges
        if limit_refresh_rate_hz:
            options.limit_refresh_rate_hz = limit_refresh_rate_hz
        
        self.matrix = RGBMatrix(options = options)

        font = graphics.Font()
        # TODO: Make path dynamic
        font.LoadFont("/home/caadmin/pi5-project/pi5board/fonts/9x18.bdf")

        self.font = font
    
    def drawText(self, richText, duration = 5):
        graphics.DrawText(self.matrix, self.font, 0, self.font.height, richText.color, richText.text)
        time.sleep(duration)
        self.matrix.Clear()
