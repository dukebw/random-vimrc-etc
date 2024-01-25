#!/bin/bash

# Check if at least one argument is provided
if [ $# -eq 0 ]; then
  echo "Usage: $0 <command>"
  exit 1
fi

# Execute the provided command in the background
"$@" &
command_pid=$!

# Wait for the command to start running
sleep 1

# Begin profiling
sudo perf record -F 99 -g -p $command_pid

# Wait for the command to complete
wait $command_pid

# Set permissions and generate flame graph
sudo chmod 777 perf.data
perf script | ../FlameGraph/stackcollapse-perf.pl > out.perf-folded
../FlameGraph/flamegraph.pl out.perf-folded > perf.svg
