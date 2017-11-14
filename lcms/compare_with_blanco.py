import numpy as np
import pandas as pd
from lcms.utils import load_df_per_exp


def get_df_mean_intensity_nlargest(df_b, df_a, n=1):
    '''
    maakt een dataframe met voor iedere stof de hoogste (n=1), of de som van de n hoogste (n>1),
    intensiteitswaardes per stof (formula) voor zowel stof a als stof b.
    vergelijkt hoeveel keer hoger (of lager) de intensiteit van dezelfde stof is ina als in b de
    target als in de b substantie


    :param df_a: data met de waardes van sample a uit de db
    :param df_b: data met de waardes van sample b uit de db
    :param n: als n == 1, wordt van iedere stof de hoogste intensiteit genomen. Als n > 1, dan
              wordt het gemiddelde van de n hoogste waardes genomen
    :return: df met de hoogste (of het gemiddelde van) intensiteit per stof voor zowel sample
             a als sample b, en het relatieve verschil tussen deze waardes.
    '''

    if n == 1:
        # groupby met de hoogste intensteit per stof, en selecteer ook de bijbehorende rt
        grouped_a = df_a.groupby('formula')[['intensity', 'rt', 'mz']].max()
        grouped_b = df_b.groupby('formula')[['intensity', 'rt', 'mz']].max()

        # hernoem de kolomnamen om verwarring tussen stof a en b te voorkomen
        new_colname = 'highest_i'
        sample = 'a'
        colname_a = '{}_{}'.format(new_colname, sample)
        colnames_a = {'intensity': colname_a, 'rt': 'rt_{}'.format(sample),
                      'mz': 'mz_{}'.format(sample)}
        grouped_a.rename(columns=colnames_a, inplace=True)

        sample = 'b'
        colname_b = '{}_{}'.format(new_colname, sample)
        colnames_b = {'intensity': colname_b, 'rt': 'rt_{}'.format(sample),
                      'mz': 'mz_{}'.format(sample)}
        grouped_b.rename(columns=colnames_b, inplace=True)
    else:
        # groupby met gemiddelde van iedere stof van de n hoogste intensity-waardes
        grouped_a = df_a.groupby('formula')['intensity'].apply(
            lambda grp: grp.nlargest(n).sum())
        grouped_b = df_b.groupby('formula')['intensity'].apply(
            lambda grp: grp.nlargest(n).sum())

        # hernoem de kolomnamen om verwarring te voorkomen
        new_colname = 'sum_i_top-{}'.format(n)
        colname_a = '{}_{}'.format(new_colname, 'a')
        grouped_a.rename(colname_a, inplace=True)
        colname_b = '{}_{}'.format(new_colname, 'b')
        grouped_b.rename(colname_b, inplace=True)

    # join de a- en b-tabel op 'formula'
    df_join = pd.concat([grouped_a,
                         grouped_b],
                        axis=1)

    # diff_factor: hoe veel vaker de stof in sample 'a' voorkomt dan in sample 'b', of andersom
    df_join['diff_factor'] = np.log(df_join[colname_a] / df_join[colname_b])
    df_join[colname_a].fillna(0, inplace=True)
    df_join[colname_b].fillna(0, inplace=True)
    df_join['a>b'] = np.where(df_join[colname_a] > df_join[colname_b], 1, 0)
    df_join['diff_factor'] = np.exp(df_join['diff_factor'].abs())
    df_join = df_join.sort_values('diff_factor', ascending=False)
    df_join = df_join.round({'diff_factor': 2})

    return df_join, new_colname


def keep_only_interesting_values(df, colname, th_diff_factor=3, th_missing=1000):
    '''
    only keep the values that are significantly different in intensity between the a and b sample

    :param df: df resulting from get_df_mean_intensity_nlargest
    :param colname: first part of the name of the intensity columns
    :param th_diff_factor: diff_factor must be equal to or larger than this threshold
    :param th_missing: the min intensity value for intensities that are missing in the other sample
    :return: df only containing formulas that are significantly more present in one of the samples than in the other
    '''

    df = df[(df['diff_factor'] >= th_diff_factor) | (df['diff_factor'].isnull())]
    df = df[(df['{}_a'.format(colname)] > th_missing) |
            (df['{}_b'.format(colname)] > th_missing)]
    return df


def get_significant_diff_between_two_samples(a_exp_id, b_exp_id):
    df_a = load_df_per_exp(a_exp_id)
    df_b = load_df_per_exp(b_exp_id)

    sample_a = df_a['filename'].iloc[0]
    sample_b = df_b['filename'].iloc[0]

    result, colname_intensity = get_df_mean_intensity_nlargest(df_a, df_b)
    out = keep_only_interesting_values(result, colname_intensity)
    return out, sample_a, sample_b


if __name__ == "__main__":
    result, sample_a, sample_b = get_significant_diff_between_two_samples(14, 16)
    print("Sample a: {}".format(sample_a))
    print("Sample b: {}".format(sample_b))
    print(result)
