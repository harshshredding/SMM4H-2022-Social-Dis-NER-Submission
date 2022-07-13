import gdown
import zipfile

url = "https://drive.google.com/file/d/1WJvM7Q7mBOp1xpyeb0zfRtvyBhQMPMt6/view?usp=sharing"
output = "gate_output.zip"
gdown.download(url=url, output=output, quiet=False, fuzzy=True)

url = "https://drive.google.com/file/d/19rZltDngthsoEgY5DSwIaviWyX5xPV8s/view?usp=sharing"
output = "data_files.zip"
gdown.download(url=url, output=output, quiet=False, fuzzy=True)

url = "https://drive.google.com/file/d/18bS-b1sXyiKV7wntyA7439UoxOIQeuJx/view?usp=sharing"
output = "embeddings.zip"
gdown.download(url=url, output=output, quiet=False, fuzzy=True)
