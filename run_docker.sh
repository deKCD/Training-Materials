#!/bin/bash
set -euo pipefail

cd /srv/jekyll

git remote set-url origin https://github.com/deKCD/Training-Materials.git

# Ensure we are on the correct branch and have the latest code before the first build
git checkout ${TARGET_BRANCH:-main}
git pull origin ${TARGET_BRANCH:-main}

export JEKYLL_ENV=production
export RACK_ENV=production

bundle exec jekyll build

bundle exec ruby webhook_server.rb &
bundle exec rackup --env production --host 0.0.0.0 --port 4000 &

wait -n
