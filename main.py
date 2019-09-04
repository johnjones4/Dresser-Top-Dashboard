from lib.dashboard_config import DashboardConfig

config = DashboardConfig("./config.yaml")
dashboard = config.generate_dashboard()
widgets = config.generate_widgets()
for widget in widgets:
  dashboard.add_widget(widget)
image = dashboard.generate()
image.save(config.get("output"))
