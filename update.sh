#!/bin/bash -u

# export LC_ALL=en_US.UTF-8
# export LANG=en_US.UTF-8

COMMAND='pipenv run kareninaclones --tweet --keyfile keys.json'
OUTFILE="$KARENINA_CLONES_LOG_DIR/error_log"

if ! $COMMAND &>"$OUTFILE"; then
  mail -s "@KareninaClones failed at $(date)" "kareninaclones@ddbeck.com" <"$OUTFILE"
fi
rm "$OUTFILE"
