source 'https://rubygems.org'

group :jekyll_plugins do
  gem 'jekyll'
  gem 'jekyll-feed'
  gem 'jekyll-sitemap'
  gem 'jekyll-redirect-from'
  gem 'jemoji'
  gem 'webrick', '~> 1.8'
end

gem 'github-pages'
gem 'connection_pool', '2.5.0'

# macOS still ships Ruby 2.6 on some systems; this keeps local preview compatible.
gem 'nokogiri', '~> 1.13.10' if Gem::Version.new(RUBY_VERSION) < Gem::Version.new('2.7')
