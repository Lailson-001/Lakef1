
#%%
import dotenv
import os
import datetime
from lakef1.collect import CollectResults
from lakef1.sender import Sender
import time

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"

dotenv.load_dotenv()

BUCKET_NAME = os.getenv("BUCKET_NAME")

# %%
while True:
    print("Iniciando o Processo")
    
    
    print("Coletando os Dados")
    colect_data = CollectResults(years=[datetime.datetime.now().year])
    colect_data.process_years()

    print("Enviando dados...")
    sender_data = Sender(bucket_name="BUCKET_NAME", bucket_folder="f1/results")
    sender_data.process_folder(DATA_DIR)
    
    print("Iteração Finalizada")
    time.sleep(60*60*6)
    
