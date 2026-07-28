#!/bin/bash
set -euo pipefail

cd /srv/jekyll

git remote set-url origin https://github.com/deKCD/Training-Materials.git

export JEKYLL_ENV=production
export RACK_ENV=production

bundle exec jekyll build

bundle exec ruby webhook_server.rb &
bundle exec rackup --env production --host 0.0.0.0 --port 4000 &

wait -n
