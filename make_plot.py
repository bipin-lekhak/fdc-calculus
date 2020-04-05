import numpy as np


from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Slider, Button, Toggle
from bokeh.plotting import figure
from copy import deepcopy as copy

np.random.seed(420)

num_points = 100
m = 2
x_line = np.arange(-1, 5.1, 0.1)
x = np.random.rand(num_points) * 5

y = m * x + np.random.randn(num_points) * 2
y_line = m * x_line

scatter_data = ColumnDataSource(data=dict(x=x, y=y))
line_data = ColumnDataSource(data=dict(x=x_line, y=y_line))


indexes = np.random.randint(num_points, size=(5,))

pair_plot = figure(
    plot_height=400,
    plot_width=400,
    title="Linear Regression",
    tools="crosshair,pan,reset,save,wheel_zoom",
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

# Set up widgets
set_m = Slider(title='m', value=m, start=0, step=0.1, end=10)
animate_button = Button(label='► Play', button_type='primary')
cluttered_button = Toggle(
    label='Filter points', button_type='primary', width=200
)


# Setup callbacks
def change_m(attr, old, new):
    new_m = set_m.value

    x_line = np.arange(-1, 5.1, 0.1)
    y_line = new_m * x_line

    line_data.data = dict(x=x_line, y=y_line)


set_m.on_change('value', change_m)


# Animate
def animate_update():
    new_m = set_m.value + .1
    if new_m > 10:
        new_m = 0
    set_m.value = new_m


def animate_button_callback():
    global callback_id
    if animate_button.label == '► Play':
        animate_button.label = '❚❚ Pause'
        callback_id = curdoc().add_periodic_callback(animate_update, 200)
    else:
        animate_button.label = '► Play'
        curdoc().remove_periodic_callback(callback_id)


animate_button.on_click(animate_button_callback)


# Clutter button
def clutter_button_callback(attr):
    if cluttered_button.active:
        scatter_data.data = {'x': x[indexes], 'y': y[indexes]}
        cluttered_button.button_type = 'success'
    else:
        scatter_data.data = {'x': x, 'y': y}
        cluttered_button.button_type = 'primary'


cluttered_button.on_click(clutter_button_callback)

layout = column(animate_button, set_m, pair_plot, cluttered_button)
curdoc().add_root(layout)
curdoc().title = "LR"
