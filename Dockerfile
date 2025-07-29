FROM ruby:3.3.9-slim-bookworm

# Install needed OS packages for Jekyll and common gems (may tweak as needed)
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
     ruby-full \ 
    build-essential \
    zlib1g-dev \
    openssl \
  && rm -rf /var/lib/apt/lists/*

RUN gem install jekyll bundler sinatra rack

# Set the working directory (inside container) for your Jekyll site
WORKDIR /srv/jekyll

COPY . .


RUN bundle install




# Default command for serving the site
# needs to be adjusted
CMD bash run_docker.sh