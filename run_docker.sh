#!/bin/bash

cd /srv/jekyll

git remote set-url origin https://github.com/deKCD/Training-Materials.git


bundle exec ruby webhook_server.rb & bundle exec jekyll serve --trace -H 0.0.0.0

wait

