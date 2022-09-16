import os
import json
import subprocess
import base64
import argparse

def getProjectRootDir():
    project_root = os.path.dirname(os.path.dirname(__file__))
    return project_root

def read_json(relativePath):
    f = open(relativePath)
    results = json.load(f)
    return results

def handleArgs():
    parser = argparse.ArgumentParser(description='Axon DataStore Creation Tool')
    parser.add_argument("-v", "--verbose", help="Displays Detailed Information", action="store_true")
    parser.add_argument("-d", "--deployEnvironment", help="Deploys Datastore to Environment", choices=['ag1', 'us2', 'us1'])
    parser.add_argument("-f", "--file", help="Input JSON File", required=True )
    parser.add_argument("--dryrun", action="store_true")
    args = parser.parse_args()

    return args