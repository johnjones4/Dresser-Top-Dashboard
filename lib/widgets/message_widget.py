from lib.widget import Widget
import requests

class MessageWidget(Widget):
  def __init__(self, font_size, font_path, inset, config):
    super().__init__("Message", font_size, font_path, inset, config)
    self.message = config["message"] if "message" in config else None
    self.url = config["url"] if "url" in config else None

  def generate_content(self, drawable, x, y, width, height):
    message = self.get_message()
    message_font_size = int(self.font_size)
    line_spacing = message_font_size * 1.25
    last_y = y + self.font_size
    text_lines = self.text_to_render_array(drawable, message, width, message_font_size)
    for line in text_lines:
      if last_y + self.font_size > y + height:
        return
      drawable.multiline_text((x,last_y), line, font=self.get_font(message_font_size), fill=0)
      last_y += line_spacing

  def get_message(self):
    if self.message is not None:
      return self.message
    if self.url is not None:
      r = requests.get(self.url)
      return r.text
