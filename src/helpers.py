import argparse
import json
import logging
import os
from datetime import datetime


def getProjectRootDir():
    project_root = os.path.dirname(os.path.dirname(__file__))
    return project_root


def read_json(relativePath):
    f = open(relativePath)
    results = json.load(f)
    return results


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
    args = parser.parse_args()

    return args


def loggerConfig(configName):
    # Set Logging
    logging.basicConfig(
        level=logging.ERROR,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(
                f'{getProjectRootDir()}/logs/{datetime.now():%Y_%m_%d_%H_%M_%S}-{configName["name"]}.log'
            ),
            logging.StreamHandler(),
        ],
    )
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    return logger
