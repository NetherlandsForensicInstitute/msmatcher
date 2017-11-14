from flask import jsonify, request

from backend import app
from lcms import utils
from lcms.visualisation.plot import peak_list_to_matrix


@app.route('/api/experiments/<id>', methods=['GET'])
def get_experiment(id=0):
    """
    retrieve experiment data of selected experiment
    data includes;
        - experiment base information
        - mz axis data
        - rt axis data
        - z values of data
    :param id: unique identifier of experiment
    :return: JSON with experiment data
    """
    matrix, rt_min_values, rt_step_size, mz_min_values, mz_step_size = peak_list_to_matrix(utils.load_peaks(id))

    response = {
        "exp_id": id,
        "meta": {
            "rt_min_values": [float(x) for x in rt_min_values],
            "rt_bin_size": rt_step_size,
            "mz_min_values": [float(x) for x in mz_min_values],
            "mz_bin_size": mz_step_size
        },
        "intensities": [list(x) for x in matrix]
    }
    return jsonify(response)


@app.route('/api/experiments', methods=['GET'])
def get_experiments():
    """
    retreives a list of all experiments in the database from the database and returns
    it via JSON
    :return: JSON(EXPERIMENTS {id: name:})
    """
    df = utils.load_experiment_names().set_index('experiment_id')['filename'].to_dict()
    response = [{'id': int(r[0]), 'name': r[1]} for r in df.items()]
    return jsonify({'experiments': response})


@app.route('/api/experiments/<id>/mz', methods=['GET'])
def get_mz_values(id=0):
    """
    retrieves all mz peaks over rt within an experiment where min_value <= mz < max_value
    makes use of request query options

    :param id: experiment id (int)
    :return: rest json with data{ experiment_id, bounds(lower, upper), points(rt, intensity, formulas) }
    """

    min_value = request.args.get("low", None, float)
    max_value = request.args.get("high", None, float)

    # catch if not a float or none given
    if min_value is None:
        min_value = -1.

    # catch if not a float or none given
    if max_value is None:
        max_value = 999999999999999.

    # build json data
    data = {
        "experiment_id": id,
        "bounds": {
            "lower": min_value,
            "upper": max_value
        },
        "points": [{'rt': r[0], 'intensity': r[1], 'formulas': r[2], 'names': r[3]} for r in
                   utils.load_peaks_for_mz(id, min_value, max_value).as_matrix()]
    }

    # build return rest-full
    return jsonify({'data': data})


@app.route('/api/experiments/<id>/rt', methods=['GET'])
def get_rt_values(id=0):
    """
    retrieves all peaks over rt within an experiment where min_value <= mz < max_value
    makes use of request query options

    :param id: experiment id (int)
    :return: rest json with data { experiment_id, bounds(lower, upper), points(rt, intensity, formulas) }
    """

    min_value = request.args.get("low", None, float)
    max_value = request.args.get("high", None, float)

    # catch if not a float or none given
    if min_value is None:
        min_value = -1.

    # catch if not a float or none given
    if max_value is None:
        max_value = 999999999999999.

    data = {
        "experiment_id": id,
        "bounds": {
            "lower": min_value,
            "upper": max_value
        },
        "points": [{'mz': r[0], 'intensity': r[1], 'formulas': r[2], 'names': r[3]} for r in
                   utils.load_peaks_for_rt(id, min_value, max_value).as_matrix()]
    }
    # build return rest-full
    return jsonify({'data': data})
