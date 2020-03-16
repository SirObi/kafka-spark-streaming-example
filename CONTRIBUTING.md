
## Directory structure
```
.
├── CONTRIBUTING.md
├── Pipfile
├── Pipfile.lock
├── README.md
├── data
│   ├── police-department-calls-for-service.json
│   └── radio_code.json
├── data_stream.py
├── kafka_server.py
├── producer_server.py
└── readme_images
    ├── kafka_topic.png
    ├── spark_output.png
    └── spark_ui.png
```

`kafka_server.py` - configures and runs the server which will upload data to Kafka broker.  

The `kafka_server` producer needs to be running while you're processing data with Spark.

Note:  
Spark Streaming pulls the data from a Kafka broker, not directly from `kafka_server`.   

`producer_server.py` defines how the data is serialized.  
It isolates the implementation of the server from the configuration code.

## Environmental variables
`$KAFKA_HOME` is wherever you unpacked (installed) Kafka. There should be a `bin` directory at this path.  
`$SPARK_HOME` is wherever you unpacked (installed) Spark. There should be a `bin` directory at this path.  

Example setup you can have in your `.bashrc` (`.zshrc`, etc...):
```
export KAFKA_HOME=/Users/dev/kafka_2.11-2.3.0
export SPARK_HOME=/Users/dev/spark-2.4.3-bin-hadoop2.7
export JAVA_HOME=/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home
export SCALA_HOME=/usr/local/scala/
export PATH=$JAVA_HOME/bin:$SPARK_HOME/bin:$SCALA_HOME/bin:$PATH
```

## Dependencies
### Java/Scala  
Kafka and Spark are written in Java/Scala, so you need to set up the environment first.  

**Spark**  
https://spark.apache.org/downloads.html  
2.3.4, prebuilt for Hadoop

**Kafka**  
https://kafka.apache.org/downloads  
2.3.0, with Scala 2.11  

**Scala**  
Download version 2.11 (Mac users can run `brew install scala@2.11`  )

**Java**  
1.8

### Python
You can install the Python dependencies to a virtual environment by running `pipenv install`.  
This is recommended, in order to keep your dependencies isolated from other projects on your machine.  
`pipenv shell` will activate the virtual environment.  
(and `exit` will let you quit the virtual env).  


## How to run it
Before you can read the Kafka server output you need to:  
- make sure your Python environment is activated  
- launch the zookeeper server  
- launch the bootstrap server  
- create a Kafka producer based on the bootstrap server  

The commands for that are as follows:  
`pipenv install` and `pipenv shell`, if you haven't already  
`$KAFKA_HOME/bin/zookeeper-server-start.sh $KAFKA_HOME/config/zookeeper.properties`  
`$KAFKA_HOME/bin/kafka-server-start.sh $KAFKA_HOME/config/server.properties`  
`python kafka_server.py`  

You can check the output of the server by running a Kafka consumer from the console:
`$KAFKA_HOME/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic udacity_projects.sf_crime_rate.pd_calls_for_service --from-beginning`  

Run:  
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.4.3  data_stream.py


Note:  
by default, the Kafka topic will only have one partition. If you want to increase number of partitions,  
you'll have to add more nodes onto the Kafka cluster. Follow the instructions here:  
https://kafka.apache.org/quickstart  

Note on Python:  
dependency isolation is key in Python. You don't want to pollute your OS's Python.  
Unless you're comfortable with Python and have your own setup, use the following guide to set up `pyenv` and `pipenv`:  
https://hackernoon.com/reaching-python-development-nirvana-bb5692adf30c


## Auto-formatting  
This project uses a Python auto-formatter called `black`.  
Simply run `black .` before commiting any new Python code.  
