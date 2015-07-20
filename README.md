Crowd Detector
===========================
### (Built Using Five Nodes on AWS)
In this project I have built and app which helps users to avoid wasting time in crowds. Imagine if we had data
about people's location. It would be nice if we could use that data to detect clusters of population. The app that
I have built takes user's location of interest in San Fransisco and a search radius seperated by comma. The result
shows the clusters of people and can look like this: 

![screenshot from 2015-06-25 22 51 03](https://cloud.githubusercontent.com/assets/9309804/8371529/fe94f456-1b8d-11e5-8042-d108b28d07fb.png)

Here are the details of how I approached this problem:

1. Data Collection: Since such data is not available to me I engineered it. I took data from Yelp which contains location
of restaurants in San Fransisco. I performed a random walk to create more points around the restaurants.

2. Here's how my pipeline looks like:

![screenshot from 2015-06-25 23 15 14](https://cloud.githubusercontent.com/assets/9309804/8371720/133ff08e-1b90-11e5-9258-b0b45afbdf7b.png)

I use Streaming K-means in the spark streaming environment. There are two indices are created on elasticsearch. 
One contains data about peoples location and is updated every day due to lack of memory storage. The other index
contains location of 1000000 people and is updated every 3 minutes.

Engineering challenges : 

1. Tunning kafka, spark streaming and elasticsearch in order to update the map as quick as possible. In particular 
tunning batch intervals has to be done carefully to avoid situations where the map is empty of points.

2. Choosing k.

