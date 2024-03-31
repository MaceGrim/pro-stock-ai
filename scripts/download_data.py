from pybaseball import statcast
import pandas as pd
import pybaseball
from tqdm import tqdm

pybaseball.cache.enable()

start_end_dates = {"2016": ["2016-04-03", "2016-10-02"],
                   "2017": ["2017-04-02", "2017-10-01"],
                   "2018": ["2018-03-29", "2018-10-01"],
                   "2019": ["2019-03-20", "2019-09-29"],
                   "2020": ["2020-07-23", "2020-09-27"],
                   "2021": ["2021-04-01", "2021-10-03"],
                   "2022": ["2022-03-31", "2022-10-02"],
                   "2023": ["2023-03-30", "2023-10-01"]}

# Sometimes the data doesn't download properly, so we'll keep trying until it does
# Because we've enabled the cache, we can start from scratch each time without taking too long

not_downloaded = True
while not_downloaded:
    try:
        results = []
        for year in tqdm(start_end_dates):
            result = statcast(start_dt=start_end_dates[year][0], end_dt=start_end_dates[year][1])
            result["year"] = int(year)
            results.append(result)
        not_downloaded = False
    except Exception as e:
        print(e)
        continue

results = pd.concat(results)

start_year = results["year"].min()
end_year = results["year"].max()

results.to_csv(f"statcast_data_{start_year}_{end_year}.csv", index=False)