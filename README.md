
# Spark Streaming - SF police calls for service
This project is an attempt to showcase an integration of Spark Streaming and Kafka.  
It uses a set of events representing the interventions of San Francisco police officers.  

## Motivation
The purpose of the project was to explore what is necessary to make Kafka and Spark Streaming work together.  
A secondary purpose was to understand what are the two most important parameters for tuning Kafka+Spark Streaming performance.  
 
## Input 
The first step in this project was to create a Kafka server which reads from a JSON file.  
The file a represents a stream of police call-for-service events from the last 3 months of 2018.  

The number of events is 199999.  
**Example event:**  
```
    {
        "crime_id": "183653763",
        "original_crime_type_name": "Traffic Stop",
        "report_date": "2018-12-31T00:00:00.000",
        "call_date": "2018-12-31T00:00:00.000",
        "offense_date": "2018-12-31T00:00:00.000",
        "call_time": "23:57",
        "call_date_time": "2018-12-31T23:57:00.000",
        "disposition": "ADM",
        "address": "Geary Bl/divisadero St",
        "city": "San Francisco",
        "state": "CA",
        "agency_id": "1",
        "address_type": "Intersection",
        "common_location": ""
    }
```

A Kafka producer ingests the data from the JSON file and stores it on the Kafka cluster.  
The input is read as a stream from the Kafka cluster, using `pyspark`.

Once you have the project set up (see instructions in [CONTRIBUTING.md](./CONTRIBUTING.md)), you should be able to view the data storied in the topic by running Kafka's CLI consumer client:  
`$KAFKA_HOME/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic udacity_projects.sf_crime_rate.pd_calls_for_service --from-beginning`  

[Events stored in Kafka topic](./readme_images/kafka_topic.png)  

## Output  

The output answers the question:  
> How many different types of crime occur in a 30-minute window, and what is the usual resolution?

[Types of crimes and actions taken, in 30-minute window](./readme_images/spark_output.png)


## Findings  
**Making Kafka and Spark Streaming work together**  
Spark Streaming already has support for Kafka. All that is necessary to do is:  
• pass the Spark package for Kafka to `spark-submit`: `--packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.4.3`  
• select Kafka as format for readStream: `df = spark.readStream.format('kafka').<other options>.load()` 

**Optimal parameters for high throughput**  
The two key things for increasing througput are:  
• the number of partitions in a Kafka topic  
• `maxOffsetsPerTrigger` in `spark.readStream`  

Rows processed per second:  
| partitions/maxOffset        | 200 | 400 | 600 | 2000 |  
| -------------               |:---:|:---:|:---:|:----:|  
| 1                           | 1   | 50  | 74  | 205  |  
| 3                           | 26  | 51  | 75  | 196  |  

In other words: parellism and batch size are important for processing speed.  
Note:  
Spark was running one executor (the "driver" executor) only (see screenshot of UI below).  
It's possible that with more executors, parallelism (~number of partitions) would play a bigger role.  

[Spark Streaming UI](./readme_images/spark_ui.png)  

## License
MIT © [Obi]()
