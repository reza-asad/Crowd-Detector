# Reza Asad
# Given a destination (lat, lon) and a coverage radius,
# this program detects the clusters of population within
# the coverage radius centered at the destination. 


import rawes
import random
import folium
import time
import json
from math import log


def push(lat, lon, coverage):
	# Connect to Elasticsearch
	es = rawes.Elastic('awsHost:9200')

	# This will clreate the map
	# extratcs points form the database and sketches them 
	# on the map.
	limit = 3000
	k = 500
	counts = [0]*k
	lats = [0]*k
	longs = [0]*k
	centroids = [[0]]*k
	rads = [0]*k

	# Query Within the Coverage distance Asked
	query = {
	  "query": {
    	"filtered" : {
    	    "query" : {
    	        "filtered" : {"filter": {"range": {
    	           "_timestamp": {
    	              "gt": "now-3m"
    	           }
    	        }}}
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

	mapPoint = es.get("real_time/people/_search?pretty=true&size={}".format(limit), data = query)
	
	j = 0
	
	# Update Information About the Detected Clusters
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
	
	# Create the Map
	USmap = folium.Map(location=[lat, lon],zoom_start=15, max_zoom=20, width=1280, height = 675)	
	for m in range(0,k):
		if(centroids[m] == [0]):
			continue
		
		rads[m] = float(log(counts[m])*log(counts[m]))/sum(counts) * 10000
		USmap.circle_marker(location= centroids[m], radius=rads[m], \
		popup='{}'.format(counts[m]), line_color='#132b5e',\
		fill_color='#132b5e', fill_opacity=0.6)
			
	USmap.create_map(path='/templates/map.html')
