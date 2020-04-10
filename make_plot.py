import numpy as np


from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Slider, Button, Toggle, glyphs
from bokeh.plotting import figure

import utils

# Initializations
np.random.seed(40)

num_points = 100
m = 3.1415
x_line = np.arange(-1, 5.1, 0.1)
x = np.random.rand(num_points) * 5

y = m * x + np.random.randn(num_points) * 2
y_line = m * x_line

scatter_data = ColumnDataSource(data=dict(x=x, y=y))
line_data = ColumnDataSource(data=dict(x=x_line, y=y_line))


indexes = np.random.randint(num_points, size=(5,))
start_m = 0
end_m = 6

# Plot scatter plot
pair_plot = figure(
    plot_height=400,
    plot_width=400,
    title="Linear Regression",
    tools="crosshair,pan,reset,save,wheel_zoom",
    x_range=[-1, 5.5],
    y_range=[-4, 20],
)

pair_plot.circle('x', 'y', source=scatter_data, color='blue')
pair_plot.line('x', 'y', source=line_data, color='red')
axis_source = ColumnDataSource(data=dict(
    xs=[[-1., 6.], [0., 0.]],
    ys=[[0., 0.], [-4., 20]],
))
axis_line = glyphs.MultiLine(
    xs='xs', ys='ys', line_color='black',
)
pair_plot.add_glyph(axis_source, axis_line)

line_x = [[i, i] for i in scatter_data.data['x']]
line_y = [
    [j, m * scatter_data.data['x'][i]]
    for i, j in enumerate(scatter_data.data['y'])
]

error_points = ColumnDataSource(data=dict(x=line_x, y=line_y))
error_glyph = glyphs.MultiLine(
    xs='x', ys='y', line_color='green', line_dash='dashed', line_alpha=0.0,
)

pair_plot.add_glyph(error_points, error_glyph)


# Plot error landscape
error_plot = figure(
    plot_height=400,
    plot_width=400,
    title="Error Plots",
    tools="crosshair,pan,reset,save,wheel_zoom",
    x_range=[start_m - 0.5, end_m + 0.5],
    y_range=[0, 50],
)
error_land_data = ColumnDataSource(data=dict(
    x=[m], y=[utils.compute_error(x, y, m)],
))
error_plot.line('x', 'y', source=error_land_data, color='red')

# Set up widgets
set_m = Slider(title='m', value=m, start=start_m, step=0.1, end=end_m)
animate_button = Button(label='► Play', button_type='primary')
cluttered_button = Toggle(
    label='Filter points', button_type='primary', width=200
)
button_draw_error = Toggle(
    label='Draw Errors', button_type='primary', width=200
)
reset_button = Button(label='Reset errors')


# Setup callbacks
def change_m(attr, old, new):
    new_m = set_m.value

    x_line = np.arange(-1, 5.1, 0.1)
    y_line = new_m * x_line

    line_data.data = dict(x=x_line, y=y_line)

    if cluttered_button.active:
        new_x = x[indexes]
        new_y = y[indexes]
    else:
        new_x = x
        new_y = y

    new_y_line = set_m.value * new_x
    new_line_x = [[i, i] for i in new_x]
    new_line_y = [[j, new_y_line[i]] for i, j in enumerate(new_y)]
    error_points.data = dict(x=new_line_x, y=new_line_y)

    error_param = np.append(error_land_data.data['x'], new_m)
    error_val = np.append(
        error_land_data.data['y'], utils.compute_error(new_x, new_y, new_m),
    )
    sort_index = np.argsort(error_param)
    error_param = error_param[sort_index]
    error_val = error_val[sort_index]
    error_land_data.data = dict(x=error_param, y=error_val)


set_m.on_change('value', change_m)


# Animate
def animate_update():
    new_m = set_m.value + .1
    if new_m > set_m.end:
        new_m = 0
    set_m.value = new_m


def animate_button_callback():
    global callback_id
    if animate_button.label == '► Play':
        animate_button.label = '❚❚ Pause'
        set_m.value = 0
        error_land_data.data = {'x': [], 'y': []}
        callback_id = curdoc().add_periodic_callback(animate_update, 50)
    else:
        animate_button.label = '► Play'
        curdoc().remove_periodic_callback(callback_id)


animate_button.on_click(animate_button_callback)


# Clutter button
def clutter_button_callback(attr):
    if cluttered_button.active:
        cluttered_button.button_type = 'success'
        scatter_data.data = {'x': x[indexes], 'y': y[indexes]}
        new_x = x[indexes]
        new_y = y[indexes]
        new_y_line = set_m.value * new_x
        new_line_x = [[i, i] for i in new_x]
        new_line_y = [[j, new_y_line[i]] for i, j in enumerate(new_y)]
        error_points.data = dict(x=new_line_x, y=new_line_y)

        error_param = error_land_data.data['x']
        error_val = [utils.compute_error(new_x, new_y, i) for i in error_param]
        error_land_data.data = dict(x=error_param, y=error_val)

    else:
        cluttered_button.button_type = 'primary'
        scatter_data.data = {'x': x, 'y': y}

        error_param = error_land_data.data['x']
        error_val = [utils.compute_error(x, y, i) for i in error_param]
        error_land_data.data = dict(x=error_param, y=error_val)


cluttered_button.on_click(clutter_button_callback)


def button_draw_error_callback(attr):
    if button_draw_error.active:
        button_draw_error.button_type = 'success'
        error_glyph.line_alpha = 1.0
    else:
        button_draw_error.button_type = 'primary'
        error_glyph.line_alpha = 0.0


button_draw_error.on_click(button_draw_error_callback)

button_row = row(cluttered_button, button_draw_error)
plots = row(pair_plot, error_plot)
layout = column(animate_button, set_m, plots, button_row)
curdoc().add_root(layout)
curdoc().title = "LR"
