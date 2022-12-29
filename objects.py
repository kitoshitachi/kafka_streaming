from torchtext.vocab import build_vocab_from_iterator
from typing import List
from torch import nn
import torch, math, re
from torch.nn import functional as F

#========================================= vocab ============================================
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


class TextClassifier(nn.Module):
    def __init__(self, name, seq_len, num_words, kernel_sizes):
        super(TextClassifier, self).__init__()
        self.name = name
        # Parameters regarding text preprocessing
        self.seq_len = seq_len
        self.num_words = num_words
        self.embedding_size = 300

        # Dropout definition
        self.dropout = nn.Dropout(0.25)

        # CNN parameters definition
        # Kernel sizes
        self.kernel_sizes = kernel_sizes

        # Output size for each convolution
        self.out_size = 2
        # Number of strides for each convolution
        self.stride = 2

        # Embedding layer definition
        self.embedding = nn.Embedding(self.num_words + 1, self.embedding_size, padding_idx=0)

        # Convolution layers definition
        self.convs = nn.ModuleList([nn.Conv1d(self.seq_len, self.out_size, kernel, self.stride) for kernel in self.kernel_sizes])

        # Max pooling layers definition
        self.pools = nn.ModuleList([nn.MaxPool1d(kernel, self.stride) for kernel in self.kernel_sizes])

        # Fully connected layer definition
        self.fc = nn.Linear(self.in_features_fc(), 1)

    def in_features_fc(self):
        '''Calculates the number of output features after Convolution + Max pooling
            
        Convolved_Features = ((embedding_size + (2 * padding) - dilation * (kernel - 1) - 1) / stride) + 1
        Pooled_Features = ((embedding_size + (2 * padding) - dilation * (kernel - 1) - 1) / stride) + 1
        
        source: https://pytorch.org/docs/stable/generated/torch.nn.Conv1d.html
        '''

        total_out_conv = 0
        for kernel in self.kernel_sizes:
            out_conv = ((self.embedding_size - 1 * (kernel - 1) - 1) / self.stride) + 1
            out_conv = math.floor(out_conv)
            out_conv = ((out_conv - 1 * (kernel - 1) - 1) / self.stride) + 1
            out_conv = math.floor(out_conv)
            total_out_conv += out_conv
        
        # Returns "flattened" vector (input for fully connected layer)
        return total_out_conv * self.out_size
  
    def forward(self, x):

        # Sequence of tokes is filterd through an embedding layer
        x = self.embedding(x)

        # Convolution layer is applied
        x = [F.relu(conv(x)) for conv in self.convs]
        x = [pool(_x) for _x, pool in zip(x, self.pools)]

        # The output of each convolutional layer is concatenated into a unique vector
        union = torch.cat(x, 2)
        union = union.reshape(union.size(0), -1)

        # The "flattened" vector is passed through a fully connected layer
        out = self.fc(union)
        # Dropout is applied		
        out = self.dropout(out)
        # Activation function is applied
        out = torch.sigmoid(out)
        
        return out.squeeze()