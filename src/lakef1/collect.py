#%%
import pandas as pd
pd.set_option('display.max_columns',None)

import fastf1

#%%
for i in range(1,50):
    
    print(f"Coletando GP {i}...")
    
    try:
        session = fastf1.get_session(2021,i,'R')
    except ValueError as err:
        print(err)
        break
        
        
    session._load_drivers_results()
    
    session.results
    session.results.to_parquet(f"../../data/2021_{i:02}_R.parquet")
    
    print(session.results)
# %%
