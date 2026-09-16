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

            # Carrega os resultados
            session._load_drivers_results()

            df = session.results.copy()
            df["Mode"] = mode

            return df

        except (ValueError, Exception) as err:
            print(f"Erro em {year}, GP={gp}, mode={mode}: {err}")
            return pd.DataFrame()

    def save_data(self, df, year, gp, mode):
        path = self.data_dir / f"{year}_{gp:02}_{mode}.parquet"
        df.to_parquet(path)
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
if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--years", "-y", nargs="+", type=int)
    parser.add_argument("--modes", "-m", nargs="+")
    args = parser.parse_args()

    collect = CollectResults(args.years, args.modes)

    collect.process_years()