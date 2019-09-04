from lib.widget import Widget
import feedparser
from dateutil import parser

class RSS_Widget(Widget):
  def __init__(self, font_size, inset, config):
    super().__init__("News", font_size, inset, config)
    self.feeds = config["feeds"]

  def generate_content(self, drawable, x, y, width, height):
    stories = self.get_news()
    headline_font_size = int(self.font_size * 1.5)
    line_spacing = headline_font_size * 1.25
    last_y = y + self.font_size
    for (headline, _) in stories:
      text_lines = self.text_to_render_array(drawable, headline, width, headline_font_size)
      if last_y + (len(text_lines) * line_spacing) > y + height:
        return
      for line in text_lines:
        drawable.multiline_text((x,last_y), line, font=self.get_font(headline_font_size), fill=0)
        last_y += line_spacing
      last_y += headline_font_size * 0.5

  def get_news(self):
    stories = set()
    for feed in self.feeds:
      d = feedparser.parse(feed)
      for entry in d["entries"]:
        stories.add((entry["title"], parser.parse(entry["published"])))
    stories_list = list(stories)
    stories_list.sort(key=lambda story: story[1], reverse=True)
    return stories_list
