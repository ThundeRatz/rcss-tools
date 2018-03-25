#!/bin/bash
set -e
cd "$(dirname "$0")"/../..

core_count=$(grep -c ^processor /proc/cpuinfo)
find -name '*.cc' | parallel -j "$core_count" g++ -Wall -Wextra -Werror -c {} -o /dev/null
