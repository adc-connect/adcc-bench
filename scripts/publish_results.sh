#!/bin/sh -xe

# Fetch most recent results
git checkout results
git pull origin results

# Deploy them to github pages
asv gh-pages --no-push --rewrite
git push -f origin gh-pages

# Checkout master again
git checkout master
