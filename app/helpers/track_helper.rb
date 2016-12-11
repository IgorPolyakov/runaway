module TrackHelper
  def avatar_url(user)
    gravatar_id = Digest::MD5::hexdigest(user.email).downcase
    # "http://gravatar.com/avatar/.png"
    "https://robohash.org/#{gravatar_id}.png"
  end
end