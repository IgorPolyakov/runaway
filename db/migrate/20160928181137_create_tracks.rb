class CreateTracks < ActiveRecord::Migration[5.0]
  def change
    create_table :tracks do |t|
      t.string :name
      t.string :description
      t.float :length
      t.float :power
      t.float :up_meter
      t.float :hour
      t.text :data
      t.binary :gpx
			t.references :user, foreign_key: true
      t.timestamps null: false
    end
  end
end
