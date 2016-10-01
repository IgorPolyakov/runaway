Runaway::Application.routes.draw do

  get '/dashboard' => 'track#index'
  get '/status' => 'track#status'
  get '/new' => 'track#new'
  get '/profile' => 'track#profile'
  post '/upload' => 'track#upload'
  get '/view' => 'track#view'
  get '/view/:id' => 'track#view'

  # root to: 'track#index'
  root to: 'runaway#start'

  get '/login' => 'sessions#new'
  post '/login' => 'sessions#create'
  get '/logout' => 'sessions#destroy'

  get '/signup' => 'users#new'
  post '/users' => 'users#create'

  get '/start' => 'runaway#start'  
  get '/about' => 'runaway#about'

end