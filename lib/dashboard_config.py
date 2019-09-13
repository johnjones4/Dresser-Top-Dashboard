import yaml
from lib.dashboard import Dashboard
from lib.widgets.wmata_widget import WMATAWidget
from lib.widgets.weather_widget import WeatherWidget
from lib.widgets.calendar_widget import CalendarWidget
from lib.widgets.rss_widget import RSSWidget
from lib.widgets.message_widget import MessageWidget

class DashboardConfig:
  def __init__(self, path):
    self.path = path
    self.load_config()

  def load_config(self):
    with open(self.path, 'r') as file:
      self.config = yaml.load(file.read(), Loader=yaml.SafeLoader)

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
    font_path = widget_global_config["font_path"]
    widgets = self.get("widgets")
    widget_instances = []
    for widget_config in widgets:
      widget = self.init_widget(widget_config["type"], font_size, font_path, padding, widget_config)
      widget_instances.append(widget)
    return widget_instances

  def init_widget(self, widget_type, font_size, font_path, padding, config):
    if widget_type == "calendar":
      return CalendarWidget(font_size, font_path, padding, config)
    elif widget_type == "wmata":
      return WMATAWidget(font_size, font_path, padding, config)
    elif widget_type == "weather":
      return WeatherWidget(font_size, font_path, padding, config)
    elif widget_type == "rss":
      return RSSWidget(font_size, font_path, padding, config)
    elif widget_type == "message":
      return MessageWidget(font_size, font_path, padding, config)
