#!/usr/bin/python
import secrets
import os

class SecureAuthentication:
   def __init__(self):
      """Load credentials from environment variables"""
      self.valid_username = os.getenv("VALID_USERNAME")
      self.valid_password = os.getenv("VALID_PASSWORD")
   def authenticate(self, username, password):
      """Use secrets.compare_digest for constant-time comparison"""
      if username == self.valid_username and secrets.compare_digest(password, self.valid_password):
         return True
      else:
         return False

if __name__ == "__main__":
   # Create an instance of SimpleAuthentication
   authentication = SecureAuthentication()
   # Get username and password from the user
   username = input("Enter your username: ")
   password = input("Enter your password: ")
   if authentication.authenticate(username, password):
      print(f"Welcome, {username}! Authentication successful.")
   else:
      print("Error: Invalid username or password. Authentication failed.")

