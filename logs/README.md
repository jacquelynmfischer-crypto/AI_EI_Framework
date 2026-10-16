# Logs

Trial data collected by hand goes here, one CSV per sub-dimension (`calibration.csv`, `faithfulness.csv`,
etc.), following the column structure specified in the matching `items/*.md` file.

`calibration_template.csv` shows the expected header row and one example row — copy it to
`calibration.csv` and fill in real trials (not committed as sample data to avoid confusion with real
results).

Raw model transcripts, if saved instead of hand-logged, go in `logs/transcripts/<model>/<item_id>_<trial_num>.txt`.
