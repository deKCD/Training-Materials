#!bin/bash

cd /src/jekyll

git remote set-url origin https://github.com/deKCD/Training-Materials.git

cd -

bundle exec ruby webhook_server.rb & bundle exec jekyll serve --trace -H 0.0.0.0

wait

