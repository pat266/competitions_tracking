import os
import time

import schedule

import competition_tracker as tracker

"""
A file to constantly retrieve the algorithms of a specific competition
and upload it to a json file every x minutes.
"""


class ScheduleRecord:
    def __init__(self):
        # change these variables to change the filename/location
        # path
        self.dir_path = "./data"
        # name of the files (i.e. team_leaderboard.json)
        self.team_file_name = "team_leaderboard"
        self.algos_file_name = "algos_leaderboard"

        # change this to get the information of a different competition
        self.competitionId = 297

    def trigger_testsuite(self):
        print("I am working as expected.")

    def schedule_get_algorithms_competition(self):
        """
        These methods are used to get the team highest elo algorithm
        """
        # get the current algorithms leaderboard from different teams
        new_team_leaderboard = tracker.get_team_leaderboard(
            competitionId=self.competitionId
        )
        new_team_leaderboard = tracker.sort_algos_dict(new_team_leaderboard)

        # check if there is a file available
        if os.path.exists(os.path.join(self.dir_path, self.team_file_name + ".json")):
            old_team_leaderboard = tracker.import_algos(
                self.dir_path, self.team_file_name
            )
            # update the old team leaderboard with the new one
            new_team_leaderboard = tracker.update_algos_dict(
                old_team_leaderboard, new_team_leaderboard
            )
        # sort it by elo
        new_team_leaderboard = tracker.sort_algos_dict(
            new_team_leaderboard, key="algo_rating"
        )
        # save it back to its location
        tracker.export_algos(new_team_leaderboard, self.dir_path, self.team_file_name)

        """
        These methods are used to get the team highest elo algorithm
        """
        # get the current algorithms leaderboard from different teams
        new_algos_leaderboard = tracker.get_competition_algorithms(
            competitionId=self.competitionId
        )
        new_algos_leaderboard = tracker.sort_algos_dict(new_algos_leaderboard)

        # check if there is a file available
        if os.path.exists(os.path.join(self.dir_path, self.algos_file_name + ".json")):
            old_algos_leaderboard = tracker.import_algos(
                self.dir_path, self.algos_file_name
            )
            # update the old team leaderboard with the new one
            new_algos_leaderboard = tracker.update_algos_dict(
                old_algos_leaderboard, new_algos_leaderboard
            )
        # sort it by elo
        new_algos_leaderboard = tracker.sort_algos_dict(
            new_algos_leaderboard, key="algo_rating"
        )
        # save it back to its location
        tracker.export_algos(new_algos_leaderboard, self.dir_path, self.algos_file_name)


if __name__ == "__main__":
    schedule_record = ScheduleRecord()
    schedule_record.schedule_get_algorithms_competition()
    # schedule.every(5).minutes.do(schedule_record.schedule_get_algorithms_competition)
    # while True:
    #     try:
    #         schedule.run_pending()
    #         schedule_record.trigger_testsuite()
    #     except Exception:
    #         print('Scheduler failed')
    #     time.sleep(1)
