#!/usr/bin/env python3
import datetime
import json
import numpy
import os
import rcss
import scipy.stats as stats


def parse_args():
    def fraction_float(n):
        n = float(n)
        if 0 <= n <= 1:
            return n
        raise argparse.ArgumentTypeError('Must be between 0 and 1')
    import argparse
    parser = argparse.ArgumentParser(description='Run team enhancement test.')
    parser.add_argument('team_a', help='Left team target program')
    parser.add_argument('team_b', help='Right team target program')
    parser.add_argument('-n', dest='match_count', type=int, default=10,
                        help='Number of matches to run')
    parser.add_argument('--significance', type=fraction_float, default=0.05,
                        help='Significance level')
    return parser.parse_args()


class ResultReportWriter:
    def __init__(self):
        self.out_dir = datetime.datetime.utcnow().isoformat()
        os.mkdir(self.out_dir)
        print('Saving results to {}'.format(self.out_dir))

    def write_json(self, filename, data):
        with open(os.path.join(self.out_dir, filename), 'w') as f:
            json.dump(data, f)


def run(args):
    report = ResultReportWriter()

    team_names, results = rcss.run_matches(args.team_a, args.team_b, args.match_count)
    report.write_json('match_results.json', {
        'binaries': [args.team_a, args.team_b],
        'teams': team_names,
        'results': results,
    })

    errors = []
    score = [x - y for x, y in results]
    # alpha, 1 - alpha
    # alpha = probability of rejecting a true null hypothesis
    significance, confidence = (args.significance, 1 - args.significance)
    _, normality_p = stats.shapiro(score)
    if normality_p <= significance:
        errors.append('Shapiro test rejected normality')
    mean = numpy.mean(score)
    std_error = stats.sem(score)
    confidence_interval = stats.t.interval(confidence, len(score) - 1,
                                           loc=mean, scale=std_error)
    report.write_json('statistics.json', {
        'binaries': [args.team_a, args.team_b],
        'teams': team_names,
        'normality_p': normality_p,
        'score': [confidence_interval[0], mean, confidence_interval[1]],
        'score_std': std_error,
        'params': {
            'significance': args.significance,
        },
        'errors': errors,
    })

if __name__ == '__main__':
    run(parse_args())
