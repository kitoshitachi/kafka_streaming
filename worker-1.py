from utils import clean_data, create_consumer, create_producer, Language
from settings import DELAY, TOPIC_PREPROCESSING, GROUP_W2V
import time, pickle

def foo(x):
    return x

def main():
    '''argv python worker.py'''
    try:
        W2V = pickle.load(open(f"model/W2V.pkl", 'rb'))

        for message in consumer:
            print(message)
            text = clean_data(message.value["text"])
            message.value['text_feature'] = W2V.text_pipeline(text)
            # producer.send(TOPIC_LOW_MODEL, message.value, message.key)s
            print(f"{message.key}: {message.value}")
            print("=====")
            time.sleep(DELAY)

    except KeyboardInterrupt:
        consumer.close()
        # producer.close()

if __name__ == "__main__":
    consumer = create_consumer(TOPIC_PREPROCESSING, GROUP_W2V)
    # producer = create_producer()
    # print(list(consumer.partitions_for_topic(TOPIC_PREPROCESSING)))
    if consumer is not None:# and producer is not None:
        main()
    else:
        print("Consumer or Producer not found!")

    print("End")

