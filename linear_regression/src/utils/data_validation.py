def validate_input_schema(df, expected_columns):
    missing =  set(expected_columns) - set(df.columns)

    if missing:
        raise ValueError(f"Missing columns : {missing}")