import yaml
from lib.dashboard import Dashboard
from lib.widgets.wmata_widget import Wmata_Widget
from lib.widgets.weather_widget import Weather_Widget
from lib.widgets.calendar_widget import Calendar_Widget
from lib.widgets.rss_widget import RSS_Widget
from lib.widgets.message_widget import Message_Widget

class DashboardConfig:
  def __init__(self, path):
    self.path = path
    self.load_config()

  def load_config(self):
    with open(self.path, 'r') as file:
      self.config = yaml.load(file.read())

  def get(self, key):
    if key not in self.config:
      raise Exception("Key \"%s\" not in config!" % (key))
    return self.config[key]

  def generate_dashboard(self):
    dashboard_config = self.get("dashboard")
    return Dashboard(
      dashboard_config["width"],
      dashboard_config["height"],
      dashboard_config["rows"],
      dashboard_config["cols"],
      dashboard_config["gutter"]
    )

  def generate_widgets(self):
    widget_global_config = self.get("widget")
    font_size = widget_global_config["font_size"]
    padding = widget_global_config["padding"]
    widgets = self.get("widgets")
    widget_instances = []
    for widget_config in widgets:
      widget = self.init_widget(widget_config["type"], font_size, padding, widget_config)
      widget_instances.append(widget)
    return widget_instances

  def init_widget(self, widget_type, font_size, padding, config):
    if widget_type == "calendar":
      return Calendar_Widget(font_size, padding, config)
    elif widget_type == "wmata":
      return Wmata_Widget(font_size, padding, config)
    elif widget_type == "weather":
      return Weather_Widget(font_size, padding, config)
    elif widget_type == "rss":
      return RSS_Widget(font_size, padding, config)
    elif widget_type == "message":
      return Message_Widget(font_size, padding, config)
