FROM ruby:2.3

ENV APP_NAME runaway

RUN apt-get update -qq && apt-get install -y build-essential

RUN apt-get install -y libpq-dev

RUN apt-get install -y libxml2-dev libxslt1-dev

RUN apt-get install -y nodejs

ADD Gemfile /$APP_NAME/Gemfile
ADD Gemfile.lock /$APP_NAME/Gemfile.lock

WORKDIR /$APP_NAME
RUN bundle install

COPY . /$APP_NAME

# RUN rake db:create

# RUN rake db:migrate

EXPOSE 3000

CMD rails server -b 0.0.0.0

# RUN bundle exec rake \
# 	RAILS_ENV=production \
# 	DATABASE_URL=postgresql://fox:fox@192.168.99.100:5702/runaway_prod \
# 	SECRET_TOKEN=pickasecuretoken \
# 	assets:precompile

# CMD bundle exec unicorn -c config/unicorn.rb
