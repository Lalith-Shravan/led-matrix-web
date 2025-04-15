from rgbmatrix import graphics

class RichText:
    def __init__(self, text, color = graphics.Color(255, 255, 255)):
        self.text = text
        self.color = color