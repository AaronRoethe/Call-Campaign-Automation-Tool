import helpers
import pipeline.clean
import pipeline.score
import pipeline.skills

# Read Agency Configuration File
args = helpers.handleArgs()
agencyConfig = helpers.read_json(args.file)["system"]


def main():
    # extract

    # process
    clean = pipeline.clean.clean()

    # group
    skilled = pipeline.skills.complex_skills(clean)

    # score by group
    scored = pipeline.score.scored_inventory(skilled)

    # log pivot results

    # load


if __name__ == "__main__":
    main()
