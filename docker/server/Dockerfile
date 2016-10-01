FROM ruby:2.1-alpine

RUN apk add --update nodejs
RUN apk add build-base

COPY Gemfile /server/Gemfile
WORKDIR /server
RUN bundle install

COPY . /server

# RUN rake db:create

# RUN rake db:migrate

CMD rails server -b 0.0.0.0

# RUN bundle exec rake \
# 	RAILS_ENV=production \
# 	DATABASE_URL=postgresql://fox:fox@192.168.99.100:5702/runaway_prod \
# 	SECRET_TOKEN=pickasecuretoken \
# 	assets:precompile

# CMD bundle exec unicorn -c config/unicorn.rb
