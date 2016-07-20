#!/usr/bin/env python3
import re
import sys
import subprocess

rcss_cmd = [
    'rcssserver', 'server::auto_mode=true', 'server::coach_w_referee=true',
    'CSVSaver::save=true', 'CSVSaver::filename=test.csv',
]


def run_match(team_a, team_b):
    cmd = [
        *rcss_cmd, 'server::team_r_start={}'.format(team_a), 'server::team_l_start={}'.format(team_b)
    ]
    print('Running match "{}"'.format(' '.join(cmd)))
    output = subprocess.check_output(cmd, universal_newlines=True).splitlines()
    for line in output:
        teams_re = re.match("\t'(.*)' vs '(.*)'$", line)
        score_re = re.match('\tScore: (\d*) - (\d*)$', line)
        if teams_re:
            teams = (teams_re.group(1), teams_re.group(2))
        elif score_re:
            score = (score_re.group(1), score_re.group(2))
    print('{}: {} - {}: {}', teams[0], score[0], teams[1], score[1])


def main():
    # Use argparse in the future, add parameter for match count
    # https://docs.python.org/3/library/argparse.html
    if len(sys.argv) != 3:
        print('Usage: {} left_team right_team'.format(sys.argv[0]))
    for _ in range(10):
        run_match(sys.argv[1], sys.argv[2])

if __name__ == '__main__':
    main()
