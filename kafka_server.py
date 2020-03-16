import producer_server
from datetime import datetime


def run_kafka_server():
    input_file = "./data/police-department-calls-for-service.json"

    created_time = datetime.now().strftime("%Y_%m_%d_%H%M%S%f")
    producer = producer_server.ProducerServer(
        input_file=input_file,
        topic="udacity_projects.sf_crime_rate.pd_calls_for_service",
        bootstrap_servers=["localhost:9092"],
        client_id="producer_client_{}".format(created_time),
    )

    return producer


def feed():
    producer = run_kafka_server()
    producer.generate_data()


if __name__ == "__main__":
    feed()
