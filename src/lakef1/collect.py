#%%
import pandas as pd
pd.set_option('display.max_columns', None)

import fastf1
import time
import argparse

from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = ROOT_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
#%%
class CollectResults:

    def __init__(self, years=[2021, 2022, 2023], modes=["R", "S"], data_dir=DATA_DIR):
        self.years = years
        self.modes = modes
        self.data_dir = Path(data_dir) 

    def get_data(self, year, gp, mode) -> pd.DataFrame:
        try:
            session = fastf1.get_session(year, gp, mode)

            session._load_drivers_results()

            df = session.results.copy()
            df["Mode"] = mode

            df["Year"] = session.date.year
            df["Date"] = session.date
            df["Mode"] = session.name
            df["RoundNumber"] = session.event["RoundNumber"]
            df["OfficialEventName"] = session.event["OfficialEventName"]
            df["EventName"] = session.event["EventName"]
            df["Country"] = session.event["Country"]
            df["Location"] = session.event["Location"]
            return df    
        except Exception as e:
            print(f"Erro ao carregar dados de {gp} {year} ({mode}): {e}")
            return pd.DataFrame()
    
    def save_data(self, df:pd.DataFrame, year:int, gp:int, mode:str):
        path = self.data_dir / f"{year}_{gp:02}_{mode}.parquet"
        df.to_parquet(path, index=False)
        return path

    def process(self, year, gp, mode):
        print(f"Processando: {year}, GP={gp}, mode={mode}")

        df = self.get_data(year, gp, mode)

        if df.empty:
            print("Sem dados.")
            return False

        self.save_data(df, year, gp, mode)
        return True

    def process_year_modes(self, year):
        for gp in range(1, 50):
            results = [self.process(year, gp, mode) for mode in self.modes]
            if not any(results):
                print(f"Fim da temporada {year} na rodada {gp}")
                break

    def process_years(self):
        for year in self.years:
            print("Coletando dados do ano{year}")
            self.process_year_modes(year)
            time.sleep(10)
#%%


parser = argparse.ArgumentParser()
parser.add_argument("--start", type=int, default=0)
parser.add_argument("--stop", type=int,  default=0)
parser.add_argument("--years", "-y", nargs="+", type=int)
parser.add_argument("--modes", "-m", nargs="+")
args = parser.parse_args()

if args.years:
    collect = CollectResults(args.years, args.modes)

elif args.start and args.stop:
    years = [i for i in range(args.start,args.stop+1)]
    collect = CollectResults(years, args.modes)


collect.process_years()