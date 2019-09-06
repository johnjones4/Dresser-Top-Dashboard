import yaml
from lib.dashboard import Dashboard
from lib.widgets.WMATAWidget import WMATAWidget
from lib.widgets.WeatherWidget import WeatherWidget
from lib.widgets.CalendarWidget import CalendarWidget
from lib.widgets.RSSWidget import RSSWidget
from lib.widgets.MessageWidget import MessageWidget

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
      return CalendarWidget(font_size, padding, config)
    elif widget_type == "wmata":
      return WMATAWidget(font_size, padding, config)
    elif widget_type == "weather":
      return WeatherWidget(font_size, padding, config)
    elif widget_type == "rss":
      return RSSWidget(font_size, padding, config)
    elif widget_type == "message":
      return MessageWidget(font_size, padding, config)
