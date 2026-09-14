from pathlib import Path
import tomllib


CONFIG_DIR = Path(__file__).parent.parent / "config"


def load_config(file_name: str) -> dict:
    """
    Load a TOML configuration file from the project's config directory.

    Args:
        file_name (str): Name of the TOML configuration file.

    Returns:
        dict: Parsed configuration data.
    """

    config_path = CONFIG_DIR / file_name

    with config_path.open("rb") as file:
        return tomllib.load(file)