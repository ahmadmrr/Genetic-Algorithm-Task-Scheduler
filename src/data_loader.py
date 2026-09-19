import pandas as pd


def load_data(file_path: str) -> pd.DataFrame:
    """
    Load data from a CSV file.
    """

    try:
        data = pd.read_csv(file_path)
        return data

    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return None

    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
        return None

    except pd.errors.ParserError:
        print("Error: There was a parsing error while reading the file.")
        return None
