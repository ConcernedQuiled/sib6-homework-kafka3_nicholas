from confluent_kafka.avro import AvroConsumer, AvroDeserializer

def read_messages():
    consumer_config = {
        "bootstrap.servers": "localhost:9092",
        "schema.registry.url": "http://localhost:8081",
        "group.id": "data-dev",
        "auto.offset.reset": "earliest"
    }

    avro_deserializer = AvroDeserializer(consumer_config)
    consumer = AvroConsumer(consumer_config, value_deserializer=avro_deserializer)

    consumer.subscribe(['bitcoin_prices'])

    while True:
        try:
            message = consumer.poll(5)
        except Exception as e:
            print(f"Exception while trying to poll messages: {e}")
        else:
            if message:
                print(f"Successfully poll a record from Kafka topic: {message.topic()}, partition: {message.partition()}, offset: {message.offset()},\n"
                      f"message key: {message.key()}, message value: {message.value()}")
                consumer.commit()
            else:
                print("No new messages at this point. Try again later ...")

    consumer.close()

if __name__ == "__main__":
    read_messages()
