#!bin/bash

bundle exec ruby webhook_server.rb & bundle exec jekyll serve --trace -H 0.0.0.0

wait

