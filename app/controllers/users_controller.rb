class UsersController < ApplicationController
  layout 'page'
  def new
  end

  def create
    user = User.new(user_params)
    if user.save
      session[:user_id] = user.id
      redirect_to '/'
      flash.now[:success] = 'Correct'
    else
      redirect_to '/signup'
      flash.now[:danger] = 'Uncorrect'
    end
  end

private

  def user_params
    params.require(:user).permit(:name, :email, :address, :data,  :password, :password_confirmation)
  end
end