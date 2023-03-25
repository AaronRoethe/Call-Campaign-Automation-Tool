import argparse
import json
import logging
from datetime import datetime
import os

from pathlib import Path

path = Path(__file__).parent.parent.resolve()

def read_json(relativePath):
    with open(path/relativePath, "r") as f:
        return json.loads(f.read())

def handleArgs():
    parser = argparse.ArgumentParser(description="ETL Ranking Tool")
    parser.add_argument(
        "-v", "--verbose", help="Displays Detailed Information", action="store_true"
    )
    parser.add_argument(
        "-d",
        "--deployEnvironment",
        help="Deploys to Environment",
        choices=["ag1", "us2", "us1"],
    )
    parser.add_argument("-f", "--file", help="Input JSON File", required=True)
    parser.add_argument("--dryrun", action="store_true")
    parser.add_argument("-l", "--log", choices=["file", "stream", "both"], default="both")
    args = parser.parse_args()

    return args


def configure_logger(cfg, options):
    logFolder = f"{path}/logs/{cfg}"
    os.makedirs(logFolder, exist_ok=True)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

    if options in ['file', 'both']:
        file_handler = logging.FileHandler(f"{logFolder}/{datetime.now():%Y_%m_%d_%H_%M_%S}.log")
        logger.addHandler(file_handler)

    if options in ['stream', 'both']:
        stream_handler = logging.StreamHandler()
        logger.addHandler(stream_handler)

    for handler in logger.handlers:
        handler.setLevel(logging.DEBUG if options in ['file', 'both'] else logging.INFO)
        handler.setFormatter(formatter)

    return logger