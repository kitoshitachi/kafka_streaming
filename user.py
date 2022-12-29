from datetime import datetime
from utils import create_producer
import csv,sys, time
from settings import DATA_DIR, DELAY, TOPIC_PREPROCESSING, DOMAINS


def main():
    '''python user.py file_name'''
    with open(f'{DATA_DIR}/{sys.argv[1]}', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        try:
            for record in reader:
                record['current_time'] = datetime.utcnow().isoformat()
                # current time, text , label , id
                producer.send(topic=TOPIC_PREPROCESSING, value=record, partition= DOMAINS.index(record['domain']))
                print(f"{record} -> {DOMAINS.index(record['domain'])}")
                print("============")
                producer.flush()
                time.sleep(DELAY)
        except KeyboardInterrupt:
            producer.close()

if __name__ == "__main__":
    producer = create_producer()
    print(len(producer.partitions_for(TOPIC_PREPROCESSING)))
    if producer is not None:
        main()
    else:
        print("Producer not found!")

    print("End!")
        
