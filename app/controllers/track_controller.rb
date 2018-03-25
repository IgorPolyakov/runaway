class TrackController < ApplicationController
  before_action :authorize

  def new
  end

  def status
    @total_power = current_user.tracks.sum(:power)
    @total_length = current_user.tracks.sum(:length)
    @total_meter_up= current_user.tracks.sum(:up_meter)
    @total_time = current_user.tracks.sum(:hour)
  end

  def view
    if params[:id]
      render :json => Track.where(id: params[:id])
    else
      render :json => Track.all
    end
  end

  def index
    @tracks = current_user.tracks
  end

  def upload
    track = Track.new(track_params)
    # File.open('/tmp/yourfile', 'w') { |file| file.write(request) }
    track.user_id = current_user.id if current_user
    track.gpx_to_json
    if track.save
      redirect_to dashboard_path
      flash.now[:success] = 'Track was add'
    else
      redirect_to new_path
      flash.now[:danger] = 'Try again'
    end
  end
private
  def track_params
    params.require(:track).permit(:name, :description, :gpx)
  end
end
