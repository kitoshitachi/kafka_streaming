DELAY = 2
NUM_PARTITIONS = 3
REPLICATION_FACTOR = 2

BOOTSTRAP_SERVERS = [
    "localhost:9092",
    "localhost:9093",
    "localhost:9094"
]

#datadir/file_name
PROJECT_DIR = 'D:/19521204/Jupyter/kafka/project/kafka_streaming/'
DATA_DIR = PROJECT_DIR + "data"
MODEL_DIR = PROJECT_DIR +'model'
DOMAINS = ["Hotel", "Restaurant", "Education"]
LABELS = ["negative","positive"]

SEED = 111

GROUP_TFIDF = "TFIDF"
GROUP_W2V = 'W2V'
GROUP_SVM = 'SVM'
GROUP_NB = 'NB'
GROUP_CNN = 'CNN'

TOPIC_PREPROCESSING = 'CLEAN_DATA'
TOPIC_LOW_MODEL = 'LOW_MODEL'
TOPIC_HIGH_MODEL = 'HIGH_MODEL'
TOPIC_RESULT= 'RESULT'