from html.parser import HTMLParser
from ..display.rich_text import RichText

from rgbmatrix import graphics

class RichTextHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.rich_text_parts = []
        self.current_color = graphics.Color(255, 255, 255)
        self.color_stack = []
        self.bold_stack = []
        self.current_bold = "normal"

    def handle_starttag(self, tag, attrs):
        if tag == "span":
            style = dict(attrs).get("style", "")
            color = self.parse_color_from_style(style)
            if color:
                self.color_stack.append(self.current_color)
                self.current_color = color
        elif tag in ["b", "strong"]:
            self.bold_stack.append(self.current_bold)
            self.current_bold = "bold"

    def handle_endtag(self, tag):
        if tag == "span" and self.color_stack:
            self.current_color = self.color_stack.pop()
        elif tag in ["b", "strong"] and self.bold_stack:
            self.current_bold = self.bold_stack.pop()

    def handle_data(self, data):
        if data.strip():  # skip whitespace-only text nodes
            self.rich_text_parts.append(RichText(data, self.current_color, self.current_bold))

    def parse_color_from_style(self, style):
        if "color" in style:
            try:
                color_str = style.split("color:")[1].split(";")[0].strip()
                if color_str.startswith("#"):
                    r = int(color_str[1:3], 16)
                    g = int(color_str[3:5], 16)
                    b = int(color_str[5:7], 16)
                    return graphics.Color(r, g, b)
            except Exception:
                pass
        return None

def html_to_rich_text(html_string):
    parser = RichTextHTMLParser()
    parser.feed(html_string)
    return parser.rich_text_parts