#!/bin/bash -u

# export LC_ALL=en_US.UTF-8
# export LANG=en_US.UTF-8

COMMAND="pipenv run kareninaclones --tweet --keyfile $KARENINA_CLONES_DIR/keys.json"
OUTFILE="$KARENINA_CLONES_DIR/error_log"

if ! $COMMAND &>"$OUTFILE"; then
  mail -s "@KareninaClones failed at $(date)" "$RECIPIENT" <"$OUTFILE"
fi
rm "$OUTFILE"
