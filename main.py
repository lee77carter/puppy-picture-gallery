# Import necessary modules and packages
from flask import Flask, render_template, request
import requests
from dog_breeds import prettify_dog_breed

# Create a Flask application instance
app = Flask("app")

# Helper function to format breed names
def check_breed(breed):
  return "/".join(breed.split("-"))

# Defines a route for the main page ("/") handling both GET and POST requests
@app.route("/", methods=["GET","POST"])
def dog_images_gallery():
  errors = []
  
  # Check if the form is submitted (POST request)
  if request.method == "POST":
    breed = request.form.get("breed")
    number = request.form.get("number")
    
    # Validate form inputs
    if not breed:
      errors.append("Oops! Please choose a breed.")
    if not number:
      errors.append("Oops! Please choose a number.")
      
    # If breed and number are provided, fetch and display dog images
    if breed and number:
      response = requests.get("https://dog.ceo/api/breed/" + check_breed(breed) + "/images/random/" + number)
      data = response.json()
      dog_images = data["message"]
      return render_template("dogs.html", images=dog_images, breed=prettify_dog_breed(breed), errors=[])
    
  # Render the main page template with or without errors  
  return render_template("dogs.html", images=[], breed="", errors=errors)

# Define a separate route for fetching a random dog image ("/random") using a POST request
@app.route("/random", methods=["POST"])
def get_random():
    response = requests.get("https://dog.ceo/api/breeds/image/random")
    data = response.json()
    dog_images = [data["message"]]
    return render_template("dogs.html", images=dog_images)

# Enable debugging and run the Flask application on specified host and port
app.debug = True
app.run(host='0.0.0.0', port=8080)