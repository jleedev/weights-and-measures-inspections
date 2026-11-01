from pathlib import Path
import tomllib

CONFIG = tomllib.load(Path("config.toml").open("rb"))
