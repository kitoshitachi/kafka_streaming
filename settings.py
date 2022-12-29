DELAY = 5
NUM_PARTITIONS = 3
REPLICATION_FACTOR = 1

BOOTSTRAP_SERVERS = [
    "localhost:9092",
    "localhost:9093",
    "localhost:9094"
]

#datadir/file_name
DATA_DIR = "D:/19521204/Jupyter/kafka/project/data"
DOMAINS = ["Hotel", "Restaurant", "Education"]
LABELS = {"negative":0,"positive":1}

SEED = 111

GROUP_TFIDF = "tfidf"
GROUP_W2V = 'W2V'
GROUP_SVM = 'SVM'
GROUP_NB = 'NB'
GROUP_CNN = 'CNN'

TOPIC_PREPROCESSING = 'preprocessing_data'
TOPIC_LOW_MODEL = 'LOW_MODEL'
TOPIC_HIGH_MODEL = 'HIGH_MODEL'