import time

from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
from PIL import Image

class LEDDisplay:
    def __init__(self,
                 font_path: str,
                 bold_font_path: str,
                 led_rows=32,
                 led_cols=64,
                 led_chain=1,
                 led_parallel=1,
                 led_pwm_bits=11,
                 led_brightness=100,
                 led_gpio_mapping="regular",
                 led_scan_mode=1,
                 led_pwm_lsb_nanoseconds=130,
                 led_show_refresh=False,
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
        font.LoadFont(font_path)

        self.font = font
        

        boldFont = graphics.Font()
        boldFont.LoadFont(bold_font_path)

        self.boldFont = boldFont
    
    def drawText(self, message):

        textLength = 0
        for richText in message:
            textLength += len(richText.text)

        fontWidth = self.font.CharacterWidth(ord('A'))
        textLength *= fontWidth

        messageXPos = 0

        nextFrame = self.matrix.CreateFrameCanvas()
        
        while abs(messageXPos) < textLength:
            richTextXPos = messageXPos
            
            for richText in message:
                graphics.DrawText(nextFrame, self.font if richText.bold == "normal" else self.boldFont, richTextXPos, self.font.height, richText.color, richText.text)
                richTextXPos += len(richText.text) * fontWidth

            self.matrix.SwapOnVSync(nextFrame, 4)
            if messageXPos == 0:
                time.sleep(0.5)
            
            nextFrame.Clear()
            messageXPos -= 1
        self.matrix.Clear()

    def displayImage(self, imageFile, duration = 5):
        image = Image.open(imageFile)

        image.thumbnail((self.matrix.width, self.matrix.height))

        self.matrix.SetImage(image.convert('RGB'))

        time.sleep(5)

        self.matrix.Clear()

    def displayAnimation(self, gifFile, duration = None):
        gif = Image.open(gifFile)

        try:
            num_frames = gif.n_frames
        except AttributeError:
            raise Exception("Image provided was not a gif.")
        
        gifFrames = []
        
        for i in range(0, num_frames):
            gif.seek(i)
            frame = gif.copy()
            frame.thumbnail((self.matrix.width, self.matrix.height))
            canvas = self.matrix.CreateFrameCanvas()
            canvas.SetImage(frame.convert("RGB"))
            gifFrames.append(canvas)
        gif.close()

        curFrame = 0

        while curFrame < num_frames - 1:
            self.matrix.SwapOnVSync(gifFrames[curFrame], 4)
            curFrame += 1

        self.matrix.Clear()