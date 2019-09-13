from PIL import Image

class Dashboard:
  def __init__(self, width, height, rows, cols, gutter):
    self.width = width
    self.height = height
    self.rows = rows
    self.cols = cols
    self.row_size = (self.height / self.rows)
    self.col_size = (self.width / self.cols)
    self.gutter = gutter
    self.widgets = []

  def add_widget(self, widget):
    (row, col, row_span, col_span) = widget.get_position()
    if row < 0 or row >= self.rows:
      raise Exception("Invalid row: %d" % (row))
    if col < 0 or col >= self.cols:
      raise Exception("Invalid col: %d" % (col))
    if row_span < 0 or row + row_span > self.rows:
      raise Exception("Invalid row span: %d" % (row_span))
    if col_span < 0 or col + col_span > self.cols:
      raise Exception("Invalid col span: %d" % (col_span))
    self.widgets.append((widget, row, col, row_span, col_span))

  def generate(self):
    mode = "L"
    color = 255
    generated_image = Image.new(mode, (self.width, self.height), color=color)
    for (widget, row, col, row_span, col_span) in self.widgets:
      x = int(self.col_size * col + (self.gutter / 2.0))
      y = int(self.row_size * row + (self.gutter / 2.0))
      width = int(self.col_size * col_span - self.gutter)
      height = int(self.row_size * row_span - self.gutter)
      image = widget.generate(mode, width, height, color)
      generated_image.paste(image, (x, y))
    return generated_image
