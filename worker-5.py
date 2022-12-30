from utils import create_consumer
from settings import TOPIC_RESULT
import sys
from pymongo import MongoClient

client = MongoClient('localhost:27017')
collection = client.review.review
print(client)
def main():
    '''argv python worker.py'''
    try:
        mapper = {}
        for message in consumer:
            record = message.value
            key = f"{record['id']}_{record['domain']}"
            if key not in mapper.keys():
                mapper[key] = {"negative":0,"positive":0}
                print(f"success: {key}")
            else:
                mapper[key][record['label']] += 1

                if mapper[key]['negative'] + mapper[key]['positive'] >= 3:
                    del mapper[key]
                    print('deleted')
                elif mapper[key][record['label']] > 1:
                    result = collection.insert_one(record)
                    print(result)

                print(mapper[key][record['label']])
                print(record)
                print("=====")
                

            # time.sleep(DELAY)

    except KeyboardInterrupt:
        consumer.close()

if __name__ == "__main__":
    consumer = create_consumer(TOPIC_RESULT, TOPIC_RESULT)
    print(consumer)
    if consumer is not None:
        main()
    else:
        print("Consumer or Producer not found!")

    print("End")

