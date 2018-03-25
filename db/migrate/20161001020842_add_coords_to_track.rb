class AddCoordsToTrack < ActiveRecord::Migration[5.0]
  def change
    add_column :tracks, :coords, :string
  end
end
