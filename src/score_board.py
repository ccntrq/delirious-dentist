import datetime
from operator import itemgetter
import os
from appdirs import user_cache_dir

import config


class ScoreBoard:
    def __init__(self):
        self.ensure_highscore_file_path_exists()

    def store_score(self, score):
        timestamp = datetime.datetime.now().strftime("%b %d %Y %H:%M:%S")
        with open(self.highscore_file_path(), "a+") as high_score_file:
            high_score_file.write(f"{score},{timestamp}\n")
        return timestamp

    def get_high_scores(self, limit=10):
        with open(self.highscore_file_path(), "r+") as high_score_file:
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

    def ensure_highscore_file_path_exists(self):
        if os.path.exists(self.highscore_file_directory()):
            return
        os.makedirs(self.highscore_file_directory())

    def highscore_file_path(self):
        return os.path.join(
            self.highscore_file_directory(), config.HIGH_SCORE_FILE_NAME
        )

    def highscore_file_directory(self):
        return user_cache_dir("delirious-dentist")
