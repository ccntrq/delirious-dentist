import datetime
from operator import itemgetter

import config


class ScoreBoard:
    def store_score(self, score):
        timestamp = datetime.datetime.now().strftime("%b %d %Y %H:%M:%S")
        with open(config.HIGH_SCORE_FILE, "a+") as high_score_file:
            high_score_file.write(f"{score},{timestamp}\n")
        return timestamp

    def get_high_scores(self, limit=10):
        with open(config.HIGH_SCORE_FILE, "r+") as high_score_file:
            lines = list(
                reversed(
                    sorted(
                        map(
                            lambda x: [int(x[0]), x[1]],
                            map(
                                lambda x: x.rstrip().split(","),
                                high_score_file.readlines(),
                            ),
                        ),
                        key=itemgetter(0),
                    )
                )
            )
            return lines[0:limit]
