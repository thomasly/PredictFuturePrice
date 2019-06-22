"""save_daily_sale_data.py
Save the sales number ordered by date
First column is date_block_num
The following columns are item sales number ordered by shop_id and item_id
e.g. columns 1~21807 are the items sold in shop 0 ordered by item_id
"""

import os
from functools import cmp_to_key

import numpy as np
import pandas as pd
from tqdm import tqdm


def create_empty_data_array(n_rows, n_groups, n_items):
  return np.zeros((n_rows, n_groups*n_items))


def create_index(df, column):
  column_ids = df[column].unique()
  column_ids.sort()
  column_index = dict()
  for i, column_id in enumerate(column_ids):
    column_index[column_id] = i
  return column_index, len(column_ids)


def create_date_index(df):
  def cmp_date(date1, date2):
    d1, m1, y1 = list(map(int, date1.split(".")))
    d2, m2, y2 = list(map(int, date2.split(".")))
    if y1 > y2:
      return 1
    elif y1 < y2:
      return -1
    else:
      if m1 > m2:
        return 1
      elif m1 < m2:
        return -1
      else:
        return d1 - d2

  dates = df.date.unique()
  dates = sorted(dates, key=cmp_to_key(cmp_date))

  date_index = dict()
  for i, date in enumerate(dates):
    date_index[date] = i
  return date_index, len(dates)


def create_daily_sale_data(csv_file):
  df = pd.read_csv(csv_file)
  item_index, n_items = create_index(df, "item_id")
  shop_index, n_shops = create_index(df, "shop_id")
  date_index, n_dates = create_date_index(df)
  data_array = create_empty_data_array(n_dates, n_shops, n_items)

  for _, row in tqdm(df.iterrows(), total=df.shape[0]):
    item_id = row["item_id"]
    shop_id = row["shop_id"]
    date = row["date"]
    item_cnt = row["item_cnt_day"]

    column = n_items*shop_index[shop_id]+item_index[item_id]
    data_array[date_index[date], column] = item_cnt

  return data_array


if __name__ == "__main__":
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument("-i", help="Filename of the input csv file")
  parser.add_argument("-f", help="Filename for saving data array.")
  args = parser.parse_args()

  data_array = create_daily_sale_data(args.i)
  np.savetxt(args.f, data_array, fmt="%d", delimiter=",")