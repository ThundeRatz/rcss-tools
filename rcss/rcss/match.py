#!/usr/bin/env python3
import re
import shutil
import subprocess


class Match:
    rcss_cmd = [
        'rcssserver', 'server::auto_mode=true', 'server::coach_w_referee=true',
        # The following report might be useful, but seems broken in latest rcssserver?
        # 'CSVSaver::save=true', 'CSVSaver::filename=match_outcome.csv',
    ]

    def __init__(self, team_a, team_b):
        self.team_a = shutil.which(team_a)
        assert self.team_a, "Can't run '{}'".format(team_a)
        self.team_b = shutil.which(team_b)
        assert self.team_b, "Can't run '{}'".format(team_b)

    def run(self):
        """Runs a match and returns rcssserver's stdout split by lines"""
        cmd = [
            *Match.rcss_cmd,
            'server::team_l_start={}'.format(self.team_a),
            'server::team_r_start={}'.format(self.team_b),
        ]
        print('Running match "{}"'.format(' '.join(cmd)))
        self.match_stdout = subprocess.check_output(cmd, universal_newlines=True).splitlines()

    def get_result(self):
        """Returns results as a tuple (team_a_score, team_b_score)"""
        score_re = re.compile('\tScore: (\d*) - (\d*)$')
        for line in self.match_stdout:
            scores = score_re.match(line)
            if scores:
                return (int(scores.group(1)), int(scores.group(2)))

    def get_team_names(self):
        """Returns team names as a tuple (team_a_name, team_b_name)"""
        teams_re = re.compile("\t'(.*)' vs '(.*)'$")
        for line in self.match_stdout:
            teams = teams_re.match(line)
            if teams:
                return (teams.group(1), teams.group(2))


def run_matches(team_a, team_b, count):
    results = [None] * count
    match = Match(team_a, team_b)
    for i in range(count):
        match.run()
        results[i] = match.get_result()
    return (match.get_team_names(), results)
