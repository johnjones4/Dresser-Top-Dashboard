from lib.widget import Widget
import requests

class WeatherWidget(Widget):
  def __init__(self, font_size, font_path, inset, config):
    super().__init__("Weather", font_size, font_path, inset, config)
    self.api_key = config['api_key']
    self.latlon = config['latlon']

  def generate_content(self, drawable, x, y, width, height):
    weather = self.get_weather()
    if weather is not None:
      current_temp_font_size = int((height - y)) - (self.font_size)
      current_temp_font = self.get_font(current_temp_font_size)
      high_low_temp_font_size = int(current_temp_font_size * 0.4)
      high_low_temp_font = self.get_font(high_low_temp_font_size)
      high_low_temp_y_pad = int(((current_temp_font_size / 2) - high_low_temp_font_size) / 2)

      (current_temp_width,_) = drawable.textsize(weather["temp"], font=current_temp_font)
      (high_temp_width,_) = drawable.textsize(weather["high"], font=high_low_temp_font)
      (low_temp_width,_) = drawable.textsize(weather["low"], font=high_low_temp_font)
      high_low_temp_width = max(high_temp_width, low_temp_width)

      current_temp_x = x + int((width - (current_temp_width + high_low_temp_width + self.inset)) / 2)
      current_temp_y = y
      drawable.text((current_temp_x, current_temp_y), weather["temp"], font=current_temp_font)

      low_temp_x = current_temp_x + current_temp_width + self.inset
      low_temp_y = y + high_low_temp_y_pad
      drawable.text((low_temp_x, low_temp_y), weather["low"], font=high_low_temp_font)

      high_temp_x = low_temp_x
      high_temp_y = y + (int(current_temp_font_size / 2) + high_low_temp_y_pad)
      drawable.text((high_temp_x, high_temp_y), weather["high"], font=high_low_temp_font)

      (description_width, _) = drawable.textsize(weather["description"], font=self.get_font())
      description_x = x + int((width - description_width) / 2)
      description_y = y + current_temp_font_size + int(self.font_size * 0.5)
      drawable.text((description_x, description_y), weather["description"], font=self.get_font())


  def get_weather(self):
    data = requests.get("https://api.darksky.net/forecast/%s/%s" % (self.api_key, self.latlon)).json()
    return {
      "description": data["daily"]["data"][0]["summary"],
      "temp": "%d°" % int(data["currently"]["temperature"]),
      "low": "Low: %d°" % int(data["daily"]["data"][0]["temperatureLow"]),
      "high": "High: %d°" % int(data["daily"]["data"][0]["temperatureHigh"])
    }
