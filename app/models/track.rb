# frozen_string_literal: true

require 'gpx'
class Track < ApplicationRecord
  belongs_to :user
  validates :gpx, presence: true

  def gpx_to_json
    fordb = []
    gpx_record = GPX::GPXFile.new(gpx_data: gpx)
    gpx_record.tracks.each do |route|
      route.points.each do |point|
        fordb << [point.lat, point.lon]
      end
      self.coords = fordb.to_json
    end
    self.length = gpx_record.distance
    self.hour = (gpx_record.tracks.first.segments.first.latest_point.time.to_i - gpx_record.tracks.first.segments.first.earliest_point.time.to_i) / 3600.0
    self.power = rand(10...42) # лень
    self.up_meter = gpx_record.tracks.first.segments.first.highest_point.elevation - gpx_record.tracks.first.segments.first.lowest_point.elevation
  end
end
