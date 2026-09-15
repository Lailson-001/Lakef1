#%%
import fastf1


from pathlib import Path
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = ROOT_DIR / "data"


import pandas as pd
pd.set_option('display.max_columns',None)
#%%
session = fastf1.get_session(2021,7,"R")
session.load()



#%%
session.results
session.results.to_parquet(DATA_DIR / "2021_07_R.Parquet")


