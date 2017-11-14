import os

import numpy as np
import plotly
import plotly.graph_objs as go

import config
from lcms import utils


def peak_list_to_matrix(data, rt_bins=75, mz_bins=75):
    """returns a matrix of binned summed intensity values for a data frame that has mz, rt and intensity columns.

    :param data: the data frame
    :param rt_bins: the number of bins in the rt axis
    :param mz_bins: the number of bins in the mz axis
    :returns (matrix_of_values, min_x_values,  x_step_size, min_y_values, y_step_size)
    """
    values = data[['rt', 'mz', 'intensity']].as_matrix()

    matrix, rt_bin_edges, mz_bin_edges = np.histogram2d(values[:, 0], values[:, 1], bins=[rt_bins, mz_bins],
                                                        weights=values[:, 2])

    # NOTE matrix has to be transposed for plotly's surface plot
    return matrix.T, rt_bin_edges[:-1], get_bin_size(rt_bin_edges), \
           mz_bin_edges[:-1], get_bin_size(mz_bin_edges)


def get_bin_size(rt_bin_edges):
    rt_bin_size = 0
    if len(rt_bin_edges) > 0:
        rt_bin_size = rt_bin_edges[1] - rt_bin_edges[0]
    return rt_bin_size


def plot_peaks_as_lines(data, filter_column='rt', shown_column='mz', filename='lines_plot', folder=config.output_path):
    unique_rt_values = data[filter_column].unique()
    unique_labels = data['label'].unique()
    color_map = dict(zip(unique_labels, ['black'] * len(unique_labels)))
    color_map['blanco'] = 'grey'
    traces = [go.Scatter(
        x=[row[shown_column], row[shown_column]],
        y=[0, row['intensity']],
        mode='lines+text',
        text=['', row['formula']],
        visible=row[filter_column] == unique_rt_values[0],
        line=dict(color=color_map[row['label']], width=1 if row['label'] == 'blanco' else 2)
    ) for i, row in data.iterrows()]

    steps = [
        dict(method='restyle',
             args=['visible', [fc == rt for fc in data[filter_column]]]
             )
        for j, rt in enumerate(unique_rt_values)
    ]

    sliders = [dict(
        active=0,
        currentvalue={"prefix": "rt: "},
        # pad={"t": 50},
        steps=steps
    )]

    updatemenus = [
        dict(
            buttons=list([
                dict(
                    args=['visible', [True for fc in data[['label', filter_column]]]],
                    label='Show blanco',
                    method='restyle'
                ),
                dict(
                    args=['visible', [fc != 'blanco' for fc in data['label']]],
                    label='Hide blanco',
                    method='restyle'
                )
            ]),
            direction='left',
            pad={'r': 10, 't': 10},
            showactive=True,
            type='buttons',
            x=0.1,
            xanchor='left',
            y=1.1,
            yanchor='top'
        ),
    ]

    layout = go.Layout(
        showlegend=False,
        xaxis=dict(title='mz'),
        yaxis=dict(title='intensity'),
        sliders=sliders,
        updatemenus=updatemenus
    )
    fig = go.Figure(data=traces, layout=layout)
    plotly.offline.plot(fig, filename=os.path.join(folder, filename + '.html'))


def example_spectrum_plotting():
    data = utils.load_peaks('random')
    data['label'] = data['label'].apply(lambda x: 'blanco' if x < 10 else '')
    plot_peaks_as_lines(data)


if __name__ == '__main__':
    example_spectrum_plotting()
