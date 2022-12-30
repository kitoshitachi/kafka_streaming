from utils import create_consumer, create_producer
from settings import DOMAINS, LABELS, TOPIC_HIGH_MODEL, GROUP_CNN, MODEL_DIR, TOPIC_RESULT
from objects import TextClassifier

import torch
def main():
    '''argv python worker.py'''
    try:
        models = {}
        for domain in DOMAINS:
            models[domain] = torch.load(f"{MODEL_DIR}/CNN_{domain}.pt")
            models[domain].eval()

        with torch.no_grad():
            for message in consumer:

                record = message.value
                record['label'] = models[record['domain']](record['text_feature']) >= 0.5
                record['label'] = LABELS[record['label']]
                del record['text_feature']
                producer.send(TOPIC_RESULT, value=record, partition= DOMAINS.index(record['domain']))
                producer.flush()

                print(f"{record['domain']}: {record['text']} -> {record['label']}")
                print("=====")
                # time.sleep(DELAY)

    except KeyboardInterrupt:
        consumer.close()
        producer.close()

if __name__ == "__main__":
    consumer = create_consumer(TOPIC_HIGH_MODEL, GROUP_CNN)
    producer = create_producer()
    if consumer is not None and producer is not None:
        main()
    else:
        print("Consumer or Producer not found!")

    print("End")

