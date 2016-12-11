class SessionsController < ApplicationController
	layout 'page'
	def new
	end

	def create
		user = User.find_by_email(params[:email])
		if user && user.authenticate(params[:password])
			session[:user_id] = user.id
			flash[:success] = 'Welcome to the Runaway App!'
			redirect_to root_path
		else
			flash[:danger] = 'Un correct login/password!'
			redirect_to login_path
		end
	end

	def destroy
		session[:user_id] = nil
		redirect_to login_path
		flash[:info] = 'You log out!'
	end

end