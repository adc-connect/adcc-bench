#!/bin/sh -xe

MACHINE=`python -c "from asv.machine import Machine; print(Machine.load('~/.asv-machine.json').machine)"`
echo "asv: "`asv --version`
echo "Machine: "$MACHINE

git clean -fxd
git checkout master
git pull origin master

. setup_environment.sh

# Run the current benchmark against the master branch
asv run || true
asv run --skip-existing-successful || true

# add results to "results" branch
git checkout results
git pull origin results
git add results/$machine
git commit -m "new results from $machine"
git push origin results
git checkout master
