from PIL import Image, ImageDraw, ImageFont

class Widget:
  def __init__(self, title, font_size, inset, config):
    self.title = title
    self.inset = inset
    self.font_size = font_size
    self.position = config["position"]

  def generate(self, mode, width, height, color):
    image = Image.new(mode, (width, height), color=color)
    drawable = ImageDraw.Draw(image)
    drawable.rectangle(((0,0), (width-1,height-1)), fill=None, outline=0, width=1)
    drawable.text((self.inset, self.inset), self.title, fill=0, font=self.get_font())
    self.generate_content(drawable, self.inset, self.inset + self.font_size, width - (self.inset * 2), height - (self.inset * 2) - self.font_size)
    return image

  def generate_content(self, drawable, x, y, width, height):
    return

  def get_font(self, ofsize=None):
    if ofsize is None:
      ofsize = self.font_size
    return ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", ofsize, 0)

  def get_position(self):
    return (self.position["row"], self.position["col"], self.position["row_span"], self.position["col_span"])

  def text_to_render_array(self, draw, text, max_width, headline_font_size):
    lines = []
    for text_line in text.split("\n"):
      current_line = []
      for word in text_line.split(" "):
        current_line_joined = " ".join(current_line)
        (width, _) = draw.multiline_textsize(current_line_joined + " " + word, font=self.get_font(headline_font_size))
        if width > max_width:
          lines.append(current_line_joined)
          current_line = [word]
        else:
          current_line.append(word)
      if len(current_line) > 0:
        lines.append(" ".join(current_line))
    return lines
