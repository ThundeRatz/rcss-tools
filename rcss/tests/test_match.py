import os
import pytest
import rcss
from unittest.mock import patch

dummy_executable = os.path.join(os.path.dirname(__file__), 'dummy.sh')
dummy_not_executable = os.path.join(os.path.dirname(__file__), '../.coveragerc')


@pytest.mark.parametrize('team_a', [dummy_executable, 'python3'])
@pytest.mark.parametrize('team_b', [dummy_executable, 'python3'])
def test_match_constructor(team_a, team_b):
    # Should accept paths to executables or locate them in PATH
    rcss.Match(team_a, team_b)


@pytest.mark.parametrize('team_a,team_b', [
    ('python3', dummy_not_executable),
    (dummy_not_executable, 'python3'),
])
def test_match_constructor_fail(team_a, team_b):
    # Should fail if file doesn't exist or is not executable
    with pytest.raises(AssertionError) as excinfo:
        rcss.Match(team_a, team_b)
    assert "Can't run " in str(excinfo.value)


@patch('subprocess.check_output')
def test_getters(mock_subprocess_check_output, rcssserver_output):
    mock_subprocess_check_output.return_value = rcssserver_output
    match = rcss.Match(dummy_executable, dummy_executable)
    match.run()

    mock_subprocess_check_output.assert_called_once_with([
        *rcss.Match.rcss_cmd,
        'server::team_l_start={}'.format(dummy_executable),
        'server::team_r_start={}'.format(dummy_executable),
    ], universal_newlines=True)
    assert match.get_result() == (0, 2)
    assert match.get_team_names() == ('test_left', 'test_right')


@pytest.mark.parametrize('teams,result', [
    (('team_left', 'team_right'), [(1, 0), (0, 1), (2, 2)]),
])
@patch('subprocess.check_output')
def test_run_matches(mock_subprocess_check_output, teams, result):
    mock_subprocess_check_output.side_effect = [
        "\tScore: {} - {}\n\t'{}' vs '{}'".format(x[0], x[1], teams[0], teams[1])
        for x in result
    ]
    output = rcss.run_matches(dummy_executable, dummy_executable, len(result))

    assert mock_subprocess_check_output.call_count == len(result)
    assert output == (teams, result)
