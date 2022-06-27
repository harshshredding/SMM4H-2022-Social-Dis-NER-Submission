import torch.nn as nn
import torch


class Embedding(nn.Module):
    def __init__(self, emb_dim, vocab_size, initialize_emb, word_to_ix):
        super(Embedding, self).__init__()
        self.embedding = nn.Embedding(vocab_size, emb_dim)
        if initialize_emb:
            inv_dic = {v: k for k, v in word_to_ix.items()}

            for key in initialize_emb.keys():
                if key in word_to_ix:
                    ind = word_to_ix[key]
                    self.embedding.weight.data[ind].copy_(torch.from_numpy(initialize_emb[key]))

    def forward(self, input):
        return self.embedding(input)


def expand_labels(batch_encoding, labels):
    """
    return a list of labels with each label in the list
    corresponding to each token in batch_encoding
    """
    new_labels = []
    for token_idx in range(len(batch_encoding.tokens())):
        word_idx = batch_encoding.token_to_word(token_idx)
        new_labels.append(labels[word_idx])
    return new_labels
