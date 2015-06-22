name := "test_means"


version := "1.0"

scalaVersion := "2.10.4"

resolvers += "Concurrent Maven Repo" at "http://conjars.org/repo"
resolvers += "gphat" at "https://raw.github.com/gphat/mvn-repo/master/releases/"

libraryDependencies ++= Seq(
"org.apache.spark" %% "spark-core" % "1.3.0" % "provided",
"org.apache.spark" % "spark-streaming_2.10" % "1.3.0" % "provided",
"org.apache.spark" % "spark-mllib_2.10" % "1.3.0" % "provided",
"org.apache.spark" % "spark-streaming-kafka_2.10" % "1.3.0",
"org.elasticsearch" % "elasticsearch-spark_2.10" % "2.1.0.Beta2",
"org.json4s" % "json4s-jackson_2.10" % "3.2.10",
"com.cloudphysics" % "jerkson_2.10" % "0.6.3",
"org.elasticsearch" % "elasticsearch-hadoop" % "2.0.0",
"wabisabi" %% "wabisabi" % "2.1.3"

)

mergeStrategy in assembly := {
  case m if m.toLowerCase.endsWith("manifest.mf")          => MergeStrategy.discard
  case m if m.toLowerCase.matches("meta-inf.*\\.sf$")      => MergeStrategy.discard
  case "log4j.properties"                                  => MergeStrategy.discard
  case m if m.toLowerCase.startsWith("meta-inf/services/") => MergeStrategy.filterDistinctLines
  case "reference.conf"                                    => MergeStrategy.concat
  case _                                                   => MergeStrategy.first
}
