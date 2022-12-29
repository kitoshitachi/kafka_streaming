from utils import clean_data, create_consumer, extract_feature, create_producer
from settings import DELAY, DOMAINS, TOPIC_PREPROCESSING, GROUP_TFIDF, TOPIC_LOW_MODEL
import time, pickle

def foo(x):
    return x

def main():
    '''argv python worker.py'''
    try:
        tfidfVector = {domain: pickle.load(open(f"model/tfidf_{domain}.pkl", 'rb')) for domain in DOMAINS}
        for message in consumer:
            record = message.value
            text = clean_data(record["text"])
            text_feature = extract_feature(text)
            record['text_feature'] = tfidfVector[record['domain']].transform(text_feature)
            
            producer.send(topic=TOPIC_LOW_MODEL, value=record, partition= DOMAINS.index(record['domain']))

            print(record['text_feature'])
            time.sleep(DELAY)

    except KeyboardInterrupt:
        consumer.close()
        # producer.close()

if __name__ == "__main__":
    consumer = create_consumer(TOPIC_PREPROCESSING, GROUP_TFIDF)
    producer = create_producer()

    if consumer is not None:# and producer is not None:
        main()
    else:
        print("Consumer or Producer not found!")

    print("End")

