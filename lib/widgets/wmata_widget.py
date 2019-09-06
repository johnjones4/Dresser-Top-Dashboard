from lib.widget import Widget
import requests

class WMATAWidget(Widget):
  def __init__(self, font_size, font_path, inset, config):
    super().__init__("Next Train", font_size, font_path, inset, config)
    self.api_key = config['api_key']
    self.station = config['station']
    self.destination = config['destination']

  def generate_content(self, drawable, x, y, width, height):
    prediction = self.get_prediction()
    if prediction is not None:
      big_font_size = height - y - self.font_size
      big_font = self.get_font(big_font_size)
      (prediction_width, _) = drawable.textsize(prediction, font=big_font)
      prediction_x = x + int((width - prediction_width) / 2)
      prediction_y = y
      drawable.text((prediction_x, prediction_y), prediction, font=big_font)

      description = "minutes until next train"
      (description_width, _) = drawable.textsize(description, font=self.get_font())
      description_x = x + int((width - description_width) / 2)
      description_y = y + big_font_size + int(self.font_size * 0.5)
      drawable.text((description_x, description_y), description, font=self.get_font())

  def get_prediction(self):
    data = requests.get("https://api.wmata.com/StationPrediction.svc/json/GetPrediction/%s" % (self.station), headers={
      "api_key": self.api_key
    }).json()
    if "Trains" in data:
      for train in data["Trains"]:
        if train["DestinationCode"] == self.destination:
          return train["Min"] if train["Min"] != "" else "?"
    return None
