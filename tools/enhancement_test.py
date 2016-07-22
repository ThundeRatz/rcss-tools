#!/usr/bin/env python3
import re
import numpy
import subprocess
import scipy.stats as stats

rcss_cmd = [
    'rcssserver', 'server::auto_mode=true', 'server::coach_w_referee=true',
    'CSVSaver::save=true', 'CSVSaver::filename=test.csv',
]


def run_match(team_a, team_b):
    cmd = [
        *rcss_cmd, 'server::team_l_start={}'.format(team_a), 'server::team_r_start={}'.format(team_b)
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
    print('{}: {} - {}: {}'.format(teams[0], score[0], teams[1], score[1]))
    result = {teams[i]: score[i] for i in range(2)}
    return result


def parse_args():
    import argparse
    # TODO Improve this code and autodetect team names
    parser = argparse.ArgumentParser(description='Run team enhancement test.')
    parser.add_argument('team_a_program', help='Left team target program')
    parser.add_argument('team_a_name', help='Left team name')
    parser.add_argument('team_b_program', help='Right team target program')
    parser.add_argument('team_b_name', help='Right team name')
    parser.add_argument('-n', dest='match_count', type=int, default=10,
                        help='Number of matches to run')
    return parser.parse_args()


def main():
    args = parse_args()
    results = [None] * args.match_count
    for i in range(args.match_count):
        scores = run_match(args.team_a_program, args.team_b_program)
        results[i] = (scores[args.team_a_name], scores[args.team_b_name])
    mean = numpy.mean(results, axis=0)
    std_error = stats.sem(results, axis=0)
    confidence_interval = [
        stats.t.interval(0.95, len(mean) - 1, loc=mean[i], scale=std_error[i]) for i in range(2)
    ]

if __name__ == '__main__':
    main()
