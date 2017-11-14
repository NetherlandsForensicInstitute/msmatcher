"""
Look through the spectra, and match the peaks in those spectra to the peaks in the reference list. 
"""
import config


def find_matching_peaks(error_rate=5e-6):
    # The following query is only fast when there is an index on formula.mass_plus/mass_minus.
    # The non-indexed version is 7 times slower
    query = """
    INSERT INTO "TrivialPeakMatch"
      SELECT s."experiment_id", "formula", s.spectrum_id, p.mz, f.mass_plus - p.mz, NULL
      FROM "Peak" AS p INNER JOIN "Spectrum" AS s ON s.spectrum_id = p.spectrum_id AND s.experiment_id = p.experiment_id, "Formula" AS f
      WHERE
      f.mass_plus BETWEEN (p.mz * (1 - 5e-6)) AND (p.mz * (1 + {}))""".format(error_rate)
    config.db_connection.execute(query)
