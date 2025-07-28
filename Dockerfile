FROM ruby:3.3.9-slim-bookworm

# Install needed OS packages for Jekyll and common gems (may tweak as needed)
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
     ruby-full \ 
    build-essential \
    zlib1g-dev \
  && rm -rf /var/lib/apt/lists/*

RUN gem install jekyll bundler

# Set the working directory (inside container) for your Jekyll site
WORKDIR /srv/jekyll


# Expose the port Jekyll serves on
EXPOSE 4000

# Default command for serving the site
# needs to be adjusted
CMD ["bundle", "install", "&&", "bundle", "exec", "jekyll", "serve"]