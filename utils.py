import socket, json, re
from kafka import KafkaProducer, KafkaConsumer, KafkaAdminClient
from settings import BOOTSTRAP_SERVERS, NUM_PARTITIONS, REPLICATION_FACTOR, DOMAINS
from kafka.errors import TopicAlreadyExistsError
from kafka.admin.new_topic import NewTopic
from pyvi.ViTokenizer import tokenize as tokenizer
from pyvi.ViPosTagger import postagging
from torchtext.vocab import build_vocab_from_iterator
from torchtext.data import get_tokenizer
from typing import List, Dict

def json_encode(data):
    return json.dumps(data).encode('utf-8')

def json_decode(data):
    return json.loads(data.decode('utf-8'))    

def create_producer():
    '''creat kafka producer
    '''
    try:
        producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVERS,
                                 client_id = socket.gethostname(),
                                 batch_size = 64000,
                                 acks = 'all',
                                 retries = 5,
                                 value_serializer=json_encode,
                                 key_serializer = json_encode,
                                 )
    except Exception as e:
        print(f"Couldn't create the producer. {e}")

        # logging.exception(f"Couldn't create the producer. {e}")
        # producer = None
    return producer


def create_consumer(topic, group_id):
    '''creat kafka consumer'''
    try:
        consumer = KafkaConsumer(topic,
            bootstrap_servers=BOOTSTRAP_SERVERS,
            group_id=group_id,
            # enable_auto_commit = True,
            # max_poll_records=1,
            # max_poll_interval_ms=5000,
            # auto_offset_reset='earliest',
            value_deserializer=json_decode,
        )
        # consumer
    except Exception as e:
        print(f"Couldn't create the consumer. {e}")
        # logging.exception(f"Couldn't create the consumer. {e}")
        # consumer = None
    return consumer

def create_topic(topic_name:str):
    client = KafkaAdminClient(bootstrap_servers=BOOTSTRAP_SERVERS)

    try:
        client.create_topics([
            NewTopic(
                name=topic_name,
                num_partitions=NUM_PARTITIONS,
                replication_factor=REPLICATION_FACTOR,
            )
        ])
        
        print("Topic created!")
    except TopicAlreadyExistsError:
        print("Topic exists!")

def delete_topic(topic_name:str):
    client = KafkaAdminClient(bootstrap_servers=BOOTSTRAP_SERVERS)
    client.delete_topics([topic_name])

def clean_data(text:str, word_segment:bool = True):
    patURL = r"(?:http://|www.)[^\"]+"
    patPrice = r'([0-9]+k?(\s?-\s?)[0-9]+\s?(k|K))|([0-9]+(.|,)?[0-9]+\s?(triệu|ngàn|trăm|k|K|))|([0-9]+(.[0-9]+)?Ä‘)|([0-9]+k)'

    text = re.sub(patPrice, ' giá_tiền ', text)
    text = re.sub(r"[0-9]+", " number ", text)
    text = re.sub(patURL,' website ',text)

    text = text.replace(' k ', ' không ')
    text = text.replace(' ko ', ' không ')
    text = text.replace(' bt ', ' bình_thường ')
    text = text.replace(' ok ', ' được ')

    text = re.sub('[^\w ]','', text) # remove all special chars except white space
    text = tokenizer(text) 
    # text = remove_stopwords(text)
    text = text.lower()
    # text = re.sub(r"\?", " \? ", text)
    text = re.sub('\\s+',' ',text) # remove multiple white spaces
    text = text.strip()
    if word_segment == False:
        return text.replace('_',' ')
    else:
        return text


def ngram_featue(text:str,N:int):
    sentence = text.split(" ")
    grams = [sentence[i:i+N] for i in range(len(sentence)-N+1)]
    result = [" ".join(gram) for gram in grams]

    return result

def get_feature(text:str):
    vocab, list_pos = postagging(text)

    result = [word for word, pos in zip(vocab, list_pos) if "N" in pos or "V" in pos or "A" in pos]

    return result + list(list_pos)


def extract_feature(text_preproced:str):
	feature = ngram_featue(text_preproced,2) + ngram_featue(text_preproced,3) + ngram_featue(text_preproced,4)
	feature += get_feature(text_preproced)
	return feature

class Language:
    def __init__(self, data:List[str], min_freq:int = 2):
        specials = ["<pad>", "<unk>",  "<sos>", "<eos>"]

        self.vocab = build_vocab_from_iterator(self.__yield_tokens(data), min_freq, specials)
        self.vocab.set_default_index(1)
    
    @staticmethod
    def __tokenizer(text:str):
        return list(map(lambda word: re.sub('_', ' ', word),text.split()))

    def __yield_tokens(self, data:List[str]):
        for line in data:
            yield self.__tokenizer(line)

    def lookup_tokens(self, vec:List[int]):
        return self.vocab.lookup_tokens(vec)

    def text_pipeline(self, sent:str) -> List[int]:
        return [2,*self.vocab.lookup_indices(self.__tokenizer(sent)),3]