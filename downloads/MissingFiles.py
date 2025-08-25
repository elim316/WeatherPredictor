import re
from pathlib import Path
from datetime import date
from collections import defaultdict

YYMM_RE = re.compile(r"(\d{6})(?=\.csv$)")
# looks for 6 digits in a row and ends with csv

def build_index(base_dir: Path):
    data = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))


    for station_dir in base_dir.iterdir():
        if not (station_dir.is_dir() and not station_dir.name.startswith(".")):
            continue
        station = station_dir.name

        for year_dir in station_dir.iterdir():
            if not (year_dir.is_dir() and not year_dir.name.startswith(".")):
                continue
            year = int(year_dir.name)

            for f in year_dir.iterdir():
                if not (f.is_file() and f.suffix.lower() == ".csv"):
                    continue

                m = YYMM_RE.search(f.name)
                if not m:
                    continue # Skipe files that dont end with m
                yyyymm = m.group(1) # match the search object
                yy = int(yyyymm[:4]) # convert first 4 characters to a year in int
                mm = int(yyyymm[4:6]) 

                # cross check yy with year and month is valid
                if yy != year or not (1 <= mm <= 12):
                    continue
                    
                data[station][year][mm].append(f)
    return data

def find_missing_months(data, today=None):
    if today is None:
        today = date.today()
    cy, cm = today.year, today.month

    missing = {}

    for station, years in data.items():
        for year, months in years.items():
            end_m = cm if year == cy else 12
            expected = set(range(1, end_m + 1))
            present = set(m for m in months.keys() if 1 <= m <= 12)
            miss = sorted(expected - present)
            if miss:
                missing.setdefault(station, {})[year] = miss
                # setdefault() -> if we've seen this staiton, return dict if not create empty {}
                # [year] = miss -> assign list of months to station's year
    return missing


base_dir = Path("downloads")
data = build_index(base_dir)
missing = find_missing_months(data)

for station, years in sorted(missing.items()):
    for year, months in sorted(years.items()):
        print(f"{station} / {year}: missing months -> {months}")