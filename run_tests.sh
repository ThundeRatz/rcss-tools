#!/bin/bash
set -e
cd "$(dirname "$0")"

tests='tests/cpp/linter.sh
tests/python/linter.sh
tests/python/run_tests.sh'

for script in $tests ; do
    echo -e "\e[96mRunning test $script\e[0m"
    $script
done
