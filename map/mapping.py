# Reza Asad
# This program simulates the movement of people on 
# the map. 


import rawes
import random
import folium
import time
from tempfile import mkstemp
from shutil import move
from os import remove, close
import json
from kafka.client import KafkaClient
from kafka.producer import SimpleProducer

kafka = KafkaClient("ec2-52-8-179-244.us-west-1.compute.amazonaws.com:9092")
producer = SimpleProducer(kafka)


def push(lat, lon, coverage):
	# Connect to Elasticsearch
	es = rawes.Elastic('http://ec2-52-8-179-244.us-west-1.compute.amazonaws.com:9200')
	#USmap = folium.Map(location=[32.848957, -86.630117], tiles='Mapbox Control Room')

	# This will clreate the map
	# extratcs points form the database and sketches them 
	# on the map.
	limit = 3000
	k = 100000
	counts = [0]*k
	lats = [0]*k
	longs = [0]*k
	centroids = [[0]]*k
	rads = [0]*k


	query = {
		"query": {
			"filtered" : {
				"query" : {
					"match_all" : {}
				},
				"filter" : {
				"geo_distance" : {
					"distance" : "{}km".format(coverage),
					"location" : {
						"lat" : lat,
						"lon" : lon
					}
				}
			}
			}
		}
	}

	mapPoint = es.get("simple/people/_search?pretty=true&size={}".format(limit), data = query)
	
	j = 0
	while True:
		j+=1
		try:
			point = mapPoint["hits"]["hits"][j]["_source"]
			cluster = point["cluster"]			
			latitude = point["location"]["lat"]
			longitude = point["location"]["lon"]
			counts[cluster] +=1
			lats[cluster] += latitude
			longs[cluster] += longitude
			centroids[cluster] = [lats[cluster]/counts[cluster], longs[cluster]/counts[cluster]] 

		except IndexError:
			break	

	USmap = folium.Map(location=[lat, lon],zoom_start=15, max_zoom=20, width=1280, height = 675)	
	for m in range(0,k):
		if(centroids[m] == [0]):
			continue
		
		rads[m] = float(counts[m])/sum(counts) * 500
		USmap.circle_marker(location= centroids[m], radius=rads[m], \
		popup='{}'.format(counts[m]), line_color='#132b5e',\
		fill_color='#132b5e', fill_opacity=0.6)
			
	USmap.create_map(path='/home/ubuntu/EngData/templates/map.html')










	
