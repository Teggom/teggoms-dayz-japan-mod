#!/bin/sh
# usage: sh spikes/W2F/run.sh <log> keys...   (build no-binarize/no-pack + verify, print failures)
cd /d/DayZ-Server_AI-20260907-MultiMap/japan_dev
LOG=$1; shift
timeout 3000 python buildings/pipeline.py "$@" --no-binarize --no-pack --jobs 4 > spikes/W2F/$LOG 2>&1
grep -E "Traceback|Error" spikes/W2F/$LOG | head -5
for f in $(ls -t data/C/_build/verify_logs | head -$#); do
  n=$(head -3 data/C/_build/verify_logs/$f | grep -o "f_[a-z0-9_]*" | head -1)
  grep -E "^FAIL" data/C/_build/verify_logs/$f | grep -v "Binarize -> ODOL" | sed "s/^/[$f] /" | cut -c1-300
done
grep "^verify:" spikes/W2F/$LOG
