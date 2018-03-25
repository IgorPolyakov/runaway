# frozen_string_literal: true

class User < ActiveRecord::Base
  has_many :tracks, dependent: :destroy
  validates :name, presence: true
  VALID_EMAIL_REGEX = /\A[\w+\-.]+@[a-z\d\-.]+\.[a-z]+\z/i
  validates :email, presence: true, format: { with: VALID_EMAIL_REGEX }, uniqueness: true
  # validates :password, presence: true
  has_secure_password
end
