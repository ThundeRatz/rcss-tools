#!/usr/bin/env python3
import rcss.tools.enhancement_test
from unittest.mock import patch

dummy_executable = 'dummy.sh'


@patch('rcss.run_matches')
@patch('rcss.tools.enhancement_test.ResultReportWriter')
def test_enhancement_test_run(mock_ResultReportWriter, mock_run_matches):
    class TestArgs:
        team_a = team_b = dummy_executable
        match_count = 5
        significance = 0.05

    results = {}

    class MockResultReportWriter:
        def __init__(self):
            pass

        def write_json(self, filename, data):
            results[filename] = data

    mock_ResultReportWriter.side_effect = MockResultReportWriter
    mock_run_matches.return_value = (('team_left', 'team_right'), [
        (2, 1), (3, 2), (5, 4), (0, 10),
    ])

    rcss.tools.enhancement_test.run(TestArgs())

    assert mock_ResultReportWriter.called_once_with()
    assert set(results) == {'match_results.json', 'statistics.json'}
    assert results['match_results.json'] == {
        'binaries': [dummy_executable, dummy_executable],
        'teams': ('team_left', 'team_right'),
        'results': [(2, 1), (3, 2), (5, 4), (0, 10)],
    }
    stats = results['statistics.json']
    assert stats['binaries'] == [dummy_executable, dummy_executable]
    assert stats['teams'] == ('team_left', 'team_right')
    assert all(x < y for x, y in zip(stats['score'], stats['score'][1:]))
    assert 'Shapiro test rejected normality' in stats['errors']
