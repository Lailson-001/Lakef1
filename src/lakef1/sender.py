#%%
import dotenv
import os
import boto3
from pathlib import Path
from tqdm import tqdm
import argparse

dotenv.load_dotenv()
# %%
AWS_KEY = os.getenv("AWS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")

# %%


from pathlib import Path

class Sender:
    def __init__(self, bucket_name, bucket_folder):
        self.bucket_name = bucket_name
        self.bucket_folder = bucket_folder
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=AWS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY,
            region_name="us-east-2",
            
        )

    def process_file(self, filename):
        file = Path(filename).name
        bucket_path = os.path.join(self.bucket_folder, file)

        try:
            self.s3.upload_file(filename, self.bucket_name, bucket_path)
        except Exception as err:
            print(err)
            return False

        os.remove(filename)
        return True
    
    
    def process_folder(self, folder):
        files = os.listdir(folder)
        for f in tqdm (files):
            self.process_file(os.path.join(folder,f)) 
    
    
    
    
    
# %%

parser = argparse.ArgumentParser()
parser.add_argument("--bucket", type=str)
parser.add_argument("--bucket_path", type=str)
parser.add_argument("--folder",default="data" ,type=str)
args = parser.parse_args()


if args.bucket:
    send = Sender(args.bucket, args.bucket_path)
    send.process_folder(args.folder)

else:
    print("sem bucket definido")
