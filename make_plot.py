import numpy as np


from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Slider, TextInput
from bokeh.plotting import figure


np.random.seed(42)

num_points = 100
m = 2
x_line = np.arange(-1, 5.1, 0.1)
x = np.random.rand(num_points) * 5

y = m * x + np.random.randn(num_points)
y_line = m * x_line

scatter_data = ColumnDataSource(data=dict(x=x, y=y))
line_data = ColumnDataSource(data=dict(x=x_line, y=y_line))

pair_plot = figure(
    plot_height=400,
    plot_width=400,
    title= "Linear Regression",
    tools= "crosshair,pan,reset,save,wheel_zoom",
    x_range=[-1, 5.5],
    y_range=[-1, np.max(y_line) * 1.25],
)

pair_plot.circle('x', 'y', source=scatter_data, color='blue')
pair_plot.line('x', 'y', source=line_data, color='red')
pair_plot.line(
    [[-1, 6], [0, 0]],
    [[0, 0], [-1, max(y_line)]],
    color='green',
)

curdoc().add_root(pair_plot)
curdoc().title = "LR"
