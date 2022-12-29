from utils import create_topic, delete_topic
from settings import TOPIC_PREPROCESSING, TOPIC_LOW_MODEL, TOPIC_HIGH_MODEL, TOPIC_RESULT
import sys
def main():
    if sys.argv[1] == "create":
        create_topic(TOPIC_PREPROCESSING)
        create_topic(TOPIC_LOW_MODEL)
        create_topic(TOPIC_HIGH_MODEL)
        create_topic(TOPIC_RESULT)


    elif sys.argv[1] == "delete":
        delete_topic(TOPIC_PREPROCESSING)
        delete_topic(TOPIC_LOW_MODEL)
        delete_topic(TOPIC_HIGH_MODEL)
        delete_topic(TOPIC_RESULT)

    else:
        print(f"{sys.argv[1]} not found!")

if __name__ == "__main__":
    '''python topic.py create'''
    main()