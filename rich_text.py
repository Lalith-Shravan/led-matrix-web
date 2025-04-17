from rgbmatrix import graphics

class RichText:
    def __init__(self, text, color = graphics.Color(255, 255, 255), bold = "normal"):
        self.text = text
        self.color = color
        self.bold = bold