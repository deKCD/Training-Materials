# frozen_string_literal: true

source "https://rubygems.org"

# Ruby2Shell (CVE-2026-132825): fixed in 3.4.13 and 4.0.10.
# Requires >= 3.4.13 and excludes the vulnerable 4.0.0-4.0.9.
ruby ">= 3.4.13", *(0..9).map { |patch| "!= 4.0.#{patch}" }

# gem "rails"

gem "jekyll", "~> 4.4.1"
gem "jekyll-theme-cayman", "~> 0.2.0"
gem "minimal-mistakes-jekyll", "~> 4.24.0"

gem "jekyll-last-modified-at"
gem "jekyll-sitemap"

gem "reveal-jekyll", "~> 0.0.2"

gem "jekyll-seo-tag"

gem "sinatra", "~> 4.2.2"

gem "rackup", "~> 2.2.1"

gem "puma", "~> 6.6.0"

gem "rack", "~> 3.2.8"