#!/usr/bin/python

class SimpleAuthentication:
   """Authentication class"""
   def __init__(self):
      """Hardcoding a sample username and password for demonstration purposes"""
      self.valid_username = "user123"
      self.valid_password = "password123"
   def authenticate(self, username, password):
      """Verify credentials"""
      if username == self.valid_username and password == self.valid_password:
         return True
      else:
         return False

if __name__ == "__main__":
   # Create an instance of SimpleAuthentication
   authentication = SimpleAuthentication()
   # Get username and password from the user
   username = input("Enter your username: ")
   password = input("Enter your password: ")
   if authentication.authenticate(username, password):
      print(f"Welcome, {username}! Authentication successful.")
   else:
      print("Error: Invalid username or password. Authentication failed.")
