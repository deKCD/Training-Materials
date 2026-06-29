#!/bin/bash

cd /srv/jekyll

git remote set-url origin https://github.com/deKCD/Training-Materials.git


bundle exec ruby webhook_server.rb & bundle exec jekyll serve --host 0.0.0.0 --port 4000 
#bundle exec ruby webhook_server.rb & bundle exec jekyll build JEKYLL_ENV=production

wait

