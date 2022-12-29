from utils import clean_data, create_consumer, create_producer, add_padding_sent
from objects import Language
from settings import DELAY, DOMAINS, TOPIC_PREPROCESSING, GROUP_W2V, TOPIC_HIGH_MODEL
import pickle
import torch

def main():
    '''argv python worker.py'''
    try:
        W2V = pickle.load(open(f"model/W2V.pkl", 'rb'))

        for message in consumer:

            record = message.value
            text = clean_data(message.value["text"])
            text = add_padding_sent(text)
            text = W2V.text_pipeline(text)
            record['text_feature'] = torch.Tensor([text]).to(torch.int64)
            
            producer.send(TOPIC_HIGH_MODEL, value=record, partition= DOMAINS.index(record['domain']))
            producer.flush()

            print(f"{record['id']}: {record['text_feature'].shape} -> {DOMAINS.index(record['domain'])}")
            print("=====")
            # time.sleep(DELAY)

    except KeyboardInterrupt:
        consumer.close()
        producer.close()

if __name__ == "__main__":
    consumer = create_consumer(TOPIC_PREPROCESSING, GROUP_W2V)
    producer = create_producer()
    if consumer is not None and producer is not None:
        main()
    else:
        print("Consumer or Producer not found!")

    print("End")

