import torch
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("using device:", device)
args = {
    "gold_file_path": "./mentions.tsv",
    "silver_file_path": "./silver_disease_mentions.tsv",
    "training_data_folder_path": "./gate-output-new-matching/train",
    "validation_data_folder_path": "./gate-output-new-matching/valid",
    # "bert_model_name": "dccuchile/bert-base-spanish-wwm-cased",
    "bert_model_name": "xlm-roberta-large",
    "bert_model_output_dim": 1024,
    "num_epochs": 15,
    "save_models_dir": "./models",
    "raw_validation_files_path": "./socialdisner-data/train-valid-txt-files/validation",
    "raw_train_files_path": "./socialdisner-data/train-valid-txt-files/training",
    "umls_embeddings_path": "./embeddings.csv",
    "testing_mode": True,
    "experiment_name": "pos_encod_no_silver_new_gaz",
    "pos_embeddings_path": './spanish_pos_emb.p',
    "disease_gazetteer_path": './dictionary_distemist.tsv',
    "errors_dir": './errors',
    "model_name": "PosEncod3ClassesNoSilverNewGaz",
    "optimizer": "Ranger"
}
default_key = "DEFAULT"
