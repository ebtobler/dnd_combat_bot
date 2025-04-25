from os import path


class StatsHelpers:

    @staticmethod
    def stats_folder_path():
        return path.dirname(__file__)
