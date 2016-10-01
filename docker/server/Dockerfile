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

ENV RAILS_ENV production

COPY . /$APP_NAME

RUN rake db:create

RUN rake db:migrate

RUN bundle exec rake assets:precompile --trace

EXPOSE 3000

CMD rails server -b 0.0.0.0
