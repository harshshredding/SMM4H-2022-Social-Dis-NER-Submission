import torch
from nn_utils import *
from models import SeqLabeler
import numpy as np
from util import *
from transformers import AutoTokenizer
from read_gate_output import *
from sklearn.metrics import accuracy_score
from train_annos import get_annos_dict
from args import args

tweet_to_annos = get_annos_dict(args['annotations_file_path'])
sample_to_token_data_train = get_train_data(args['training_data_folder_path'])
sample_to_token_data_valid = get_valid_data(args['validation_data_folder_path'])
bert_tokenizer = AutoTokenizer.from_pretrained(args['bert_model_name'])
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("using device:", device)
model = SeqLabeler(1, 128, 1, 2).to(device)
loss_function = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-5)
for epoch in range(args['num_epochs']):
    epoch_loss = []
    # Training starts
    model.train()
    for sample_id in sample_to_token_data_train:
        optimizer.zero_grad()
        tokens = get_token_strings(sample_to_token_data_train[sample_id])
        labels = get_labels(sample_to_token_data_train[sample_id])
        batch_encoding = bert_tokenizer(tokens, return_tensors="pt", is_split_into_words=True,
                                        add_special_tokens=False, truncation=True, max_length=512).to(device)
        expanded_labels = expand_labels(batch_encoding, labels)
        expanded_labels = [0 if label == 'o' else 1 for label in expanded_labels]
        expanded_labels = torch.tensor(expanded_labels).to(device)
        output = model(batch_encoding)
        loss = loss_function(output, expanded_labels)
        loss.backward()
        optimizer.step()
        epoch_loss.append(loss.cpu().detach().numpy())
        break
    print(f"Epoch {epoch} Loss : {np.array(epoch_loss).mean()}")
    torch.save(model.state_dict(), args['save_models_dir'] + f'/Epoch_{epoch}')
    # Validation starts
    model.eval()
    with torch.no_grad():
        token_level_accuracy_list = []
        f1_list = []
        for sample_id in sample_to_token_data_valid:
            token_data = sample_to_token_data_valid[sample_id]
            tokens = get_token_strings(token_data)
            labels = get_labels(token_data)
            offsets_list = get_token_offsets(token_data)
            assert len(tokens) == len(labels) == len(offsets_list)
            batch_encoding = bert_tokenizer(tokens, return_tensors="pt", is_split_into_words=True,
                                            add_special_tokens=False, truncation=True, max_length=512).to(device)
            expanded_labels = expand_labels(batch_encoding, labels)
            expanded_labels = [0 if label == 'o' else 1 for label in expanded_labels]
            output = model(batch_encoding)
            pred_labels_expanded = torch.argmax(output, dim=1).detach().numpy()
            token_level_accuracy = accuracy_score(list(pred_labels_expanded), list(expanded_labels))
            token_level_accuracy_list.append(token_level_accuracy)
            pred_spans_token_index = get_spans_from_seq_labels(pred_labels_expanded, batch_encoding)
            pred_spans_char_offsets = [(offsets_list[span[0]][0], offsets_list[span[1]][1]) for span in
                                       pred_spans_token_index]
            label_spans_token_index = get_spans_from_seq_labels(expanded_labels, batch_encoding)
            label_spans_char_offsets = [(offsets_list[span[0]][0], offsets_list[span[1]][1]) for span in
                                        label_spans_token_index]
            gold_annos = tweet_to_annos.get(sample_id, [])
            gold_spans_char_offsets = [(anno['begin'], anno['end']) for anno in gold_annos]
            label_spans_set = set(label_spans_char_offsets)
            gold_spans_set = set(gold_spans_char_offsets)
            pred_spans_set = set(pred_spans_char_offsets)
            TP = len(gold_spans_set.intersection(pred_spans_set))
            FP = len(pred_spans_set.difference(gold_spans_set))
            FN = len(gold_spans_set.difference(pred_spans_set))
            TN = 0
            F1 = f1(TP, FP, FN)
            f1_list.append(F1)
            break
        print("Token Level Accuracy", np.array(token_level_accuracy_list).mean())
        print("F1", np.array(f1_list).mean())
