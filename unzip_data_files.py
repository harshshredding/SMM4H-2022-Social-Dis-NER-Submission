import zipfile

with zipfile.ZipFile('./gate_output.zip', 'r') as zip_ref:
    zip_ref.extractall('./')

with zipfile.ZipFile('./embeddings.zip', 'r') as zip_ref:
    zip_ref.extractall('./')

with zipfile.ZipFile('./data_files.zip', 'r') as zip_ref:
    zip_ref.extractall('./')

with zipfile.ZipFile('./test_data.zip', 'r') as zip_ref:
    zip_ref.extractall('./')

with zipfile.ZipFile('./gate-output-test.zip', 'r') as zip_ref:
    zip_ref.extractall('./')
