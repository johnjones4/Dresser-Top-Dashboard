from lib.dashboard_config import DashboardConfig
import sys

config = DashboardConfig("./config.yaml", sys.argv)
dashboard = config.generate_dashboard()
widgets = config.generate_widgets()
for widget in widgets:
  dashboard.add_widget(widget)
image = dashboard.generate()
image.save(config.get("output"))
