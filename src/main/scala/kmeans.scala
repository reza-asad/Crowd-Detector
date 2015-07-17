/**
 * Reza Asad
 * 
 * This computes Streaming K-means on the data consumed. 
 * Moreover each data point is marked with the cluster 
 * that it belongs to. The reslut is sent to elasticsearch
 * 
 * The rows of the training data must be vector data in the form
 * `[x1,x2,x3,...,xn]`
 * Where n is the number of dimensions.
 *
 * The rows of the test data must be labeled data in the form
 * `(y,[x1,x2,x3,...,xn])`
 * Where y is some identifier. n must be the same for train and test.
 *
 */

import kafka.serializer.StringDecoder
import org.apache.spark.SparkConf
import org.apache.spark.mllib.clustering.StreamingKMeans
import org.apache.spark.streaming.kafka._
import org.apache.spark.streaming._
import org.apache.spark.rdd.RDD
import org.apache.spark.SparkContext._
import org.apache.spark.mllib.linalg.Vectors
import org.apache.spark.mllib.regression.LabeledPoint
import org.apache.spark.streaming.{Seconds, StreamingContext}
import org.elasticsearch.spark._
import org.json4s._
import org.json4s.jackson.JsonMethods._
import org.json4s.JsonDSL._
import com.codahale.jerkson.Json
import org.apache.spark.streaming.StreamingContext._
import scala.concurrent.Await
import scala.concurrent.duration._
import scala.concurrent.ExecutionContext.Implicits.global


  def main(args: Array[String]) {
  	  
    val brokers = "awsHost:9092"
    val topics = "crowd"
    val topicsSet = topics.split(",").toSet
	
    val sparkConf = new SparkConf().setAppName("kmeans")
  	sparkConf.set("es.index.auto.create", "true")
  	sparkConf.set("es.nodes", "localhost:9200") 
  	sparkConf.set("spark.executor.memory", "5g")
  	sparkConf.set("spark.cores.max", "8")
  	sparkConf.set("spark.streaming.receiver.maxRate", "3800")
    
    // Create context with 50 seconds batch interval
    val ssc = new StreamingContext(sparkConf, Seconds(50.toLong))
    
    // Create direct kafka stream with brokers and topics
	val kafkaParams = Map[String, String]("metadata.broker.list" -> brokers)
	val messages = KafkaUtils.createDirectStream[String, String, StringDecoder, StringDecoder](ssc,kafkaParams, topicsSet).map(_._2)	
	val points = messages.map(x => parse(x))
    
    // Create Training and Test Data
    val trainingData = points.map(x => Vectors.sparse(2,Seq((0,compact(render(x \ "latitude")).toDouble),
	(1,compact(render(x \ "longitude")).toDouble))))	

    val testData = points.map(x => LabeledPoint(compact(render(x \ "id")).toInt, Vectors.sparse(2,Seq(
	(0,compact(render(x \ "latitude")).toDouble),
	(1,compact(render(x \ "longitude")).toDouble)))))


    // Build the Model    
    val model = new StreamingKMeans()
      .setK(500.toInt)
      .setDecayFactor(5)
      .setRandomCenters(2.toInt, 0.0)
    model.trainOn(trainingData)

    // Predict on Test Data
    val prediction = model.predictOnValues(testData.map(lp => (lp.label, lp.features)))

    val tupleData = points.map(x => (compact(render(x \ "id")).toDouble,
	(compact(render(x \ "latitude")).toDouble,
	 compact(render(x \ "longitude")).toDouble)))

    // Add "Cluster" as a New Field To Data	
    val data = tupleData.join(prediction)
    val output = data.map(x => Map("id"-> x._1.toInt,
	"cluster"->x._2._2,
	"location"-> Map("lat"->x._2._1._1, "lon"->x._2._1._2)))

    // Send Data to Elasticsearch	
    output.foreachRDD { rdd => {
	rdd.saveToEs("real_time/people")
	rdd.saveToEs("raw_data/people_tracks")
	}
    }

    
    ssc.start()
    ssc.awaitTermination()
  }
}
