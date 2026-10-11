import os
import pandas as pd
from utils.file_security import resolve_contained_path, validate_output_filename


OUTPUT_FOLDER = "cleaned_files"

os.makedirs(
    OUTPUT_FOLDER,
    exist_ok=True
)


def clean_data(file):
    """
    Clean uploaded CSV or Excel file.
    """

    validate_output_filename(file.filename)

    try:

        if file.filename.endswith(".csv"):
            df = pd.read_csv(file.file)
            extension = ".csv"

        elif file.filename.endswith(".xlsx"):
            df = pd.read_excel(file.file)
            extension = ".xlsx"

        else:
            raise ValueError(
                "Only CSV and Excel files are supported."
            )

    except Exception:
        raise ValueError(
            "Unable to read uploaded file."
        )

    # Strip whitespace from column names
    df.columns = df.columns.astype(str).str.strip()

    # Remove empty columns
    df = df.loc[
        :,
        ~df.columns.str.contains(
            r"^Unnamed",
            case=False
        )
    ]
    df = df.dropna(how="all", axis=1)

    original_rows = len(df)

    duplicates_removed = int(
        df.duplicated().sum()
    )

    df = df.drop_duplicates()

    # Missing Value Report
    missing_value_report = {
        column.strip().lower().replace(" ", "_"): int(count)
        for column, count in df.isnull().sum().items()
    }

    missing_values_filled = sum(
        missing_value_report.values()
    )

    df = df.fillna("N/A")

    # Clean column names
    df.columns = [
        column.strip().lower().replace(" ", "_")
        for column in df.columns
    ]

    cleaned_rows = len(df)

    total_columns = len(df.columns)

    column_names = list(df.columns)

    data_types = {
        column: str(dtype)
        for column, dtype in df.dtypes.items()
    }

    # Statistics
    statistics = {}

    numeric_columns = df.select_dtypes(
        include=["number"]
    )

    for column in numeric_columns.columns:

        statistics[column] = {
            "mean": round(float(df[column].mean()), 2),
            "median": round(float(df[column].median()), 2),
            "min": float(df[column].min()),
            "max": float(df[column].max()),
            "std": round(float(df[column].std()), 2)
        }

    preview = df.head(5).to_dict(
        orient="records"
    )

    filename = (
        os.path.splitext(file.filename)[0]
        + "_cleaned"
        + extension
    )

    filepath = resolve_contained_path(OUTPUT_FOLDER, filename)

    if extension == ".csv":
        df.to_csv(
            str(filepath),
            index=False
        )

    else:
        df.to_excel(
            str(filepath),
            index=False
        )

    return {
        "message": "Data cleaned successfully.",
        "original_rows": original_rows,
        "cleaned_rows": cleaned_rows,
        "duplicates_removed": duplicates_removed,
        "missing_values_filled": missing_values_filled,
        "total_columns": total_columns,
        "column_names": column_names,
        "data_types": data_types,
        "missing_value_report": missing_value_report,
        "statistics": statistics,
        "filename": filename,
        "preview": preview
    }
