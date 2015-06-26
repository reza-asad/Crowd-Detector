# Reza Asad
# This program creates a website for my Insight Project
# You can access my slides, demo video and my Linkedin 
# page through the website. 

import rawes
import random
import folium
import time

from mapping import push
from geopy.geocoders import Nominatim
from flask import Flask, render_template, request, redirect


app = Flask(__name__)        

@app.route('/Slides')
def slides():
    return redirect("http://www.slideshare.net/upload?origin=nav", code=302)

@app.route('/Demo')
def demo():
    return redirect("http://www.slideshare.net/upload?origin=nav", code=302)

@app.route('/Contact')
def contact():
    return redirect("https://ca.linkedin.com/in/rezaasad", code=302)

@app.route('/search')
def my_form():
    return render_template("search.html")

@app.route('/map', methods=['POST'])
def my_form_post():
	text = request.form['search']
	inputs = text.split(',')

	geolocator = Nominatim()
	location = geolocator.geocode(inputs[0])
	lat = location.latitude
	lon = location.longitude
	coverage = inputs[1]
	push(lat,lon,coverage)

	return render_template('map.html')
	

def replace(file_path, pattern, subst):
    #Create temp file
    fh, abs_path = mkstemp()
    with open(abs_path,'w') as new_file:
        with open(file_path) as old_file:
            for line in old_file:
                new_file.write(line.replace(pattern, subst))
    close(fh)
    #Remove original file
    remove(file_path)
    #Move new file
    move(abs_path, file_path)
			
if __name__ == "__main__": 
    app.run(host='0.0.0.0', debug=True)
    
    
