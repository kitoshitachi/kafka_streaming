from utils import create_consumer, create_producer
from settings import DOMAINS, TOPIC_LOW_MODEL, GROUP_SVM, MODEL_DIR, TOPIC_RESULT, LABELS
import pickle

def main():
    '''argv python worker.py'''
    try:
        models = {domain: pickle.load(open(f"{MODEL_DIR}/nb_{domain}.pkl",'rb')) for domain in DOMAINS}

        for message in consumer:

            record = message.value
            record['label'] = LABELS[models[record['domain']].predict(record['text_feature'])[0]]
            producer.send(TOPIC_RESULT, value=record, partition= DOMAINS.index(record['domain']))
            producer.flush()

            print(f"{record['domain']}: {record['text']} -> {record['label']}")
            print("=====")
            # time.sleep(DELAY)

    except KeyboardInterrupt:
        consumer.close()
        producer.close()

if __name__ == "__main__":
    consumer = create_consumer(TOPIC_LOW_MODEL, GROUP_SVM)
    producer = create_producer()
    if consumer is not None and producer is not None:
        main()
    else:
        print("Consumer or Producer not found!")

    print("End")

