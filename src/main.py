import json

import pipeline.clean
import pipeline.extract
import pipeline.score
import pipeline.skills
import utils

# Read Agency Configuration File

def main():
    args = utils.handleArgs()
    cfg = utils.read_json(args.file)
    logger = utils.configure_logger(cfg['name'], args.log)
    logger.info(json.dumps(cfg, indent=4))
    # extract
    data = pipeline.extract.get(cfg)
    # process
    # clean = pipeline.clean.clean()

    # group
    # skilled = pipeline.skills.complex_skills(clean)

    # score by group
    # scored = pipeline.score.scored_inventory(skilled)

    # log pivot results

    # load

if __name__ == "__main__":
    main()
