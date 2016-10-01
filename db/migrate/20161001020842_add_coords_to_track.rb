class AddCoordsToTrack < ActiveRecord::Migration
  def change
    add_column :tracks, :coords, :string
  end
end
