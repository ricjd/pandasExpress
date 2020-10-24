import numpy as np
import pandas as pd
from collections import defaultdict
import json

def map(df, in_column, out_column, map, default):
  map = defaultdict(
    lambda: default,
    map
  )
  df[out_column] = df[in_column].map(map)

def math(df, in_value_1, in_value_2, out_column, operator):
  print(type(in_value_1), type(in_value_2))
  if (type(in_value_1) == str):
    in_value_1 = df[in_value_1]
  if (type(in_value_2) == str):
    in_value_2 = df[in_value_2]

  if (operator == '*'):
    df[out_column] = in_value_1 * in_value_2
    return
  elif (operator == '+'):
    df[out_column] = in_value_1 + in_value_2
    return
  elif (operator == '-'):
    df[out_column] = in_value_1 - in_value_2
    return
  elif (operator == '/'):
    df[out_column] = in_value_1 / in_value_2
    return

def convert_int(df, in_column, out_column):
  df[out_column] = pd.to_numeric(df[in_column], downcast='integer')

def meta(df, columns):
  df['meta'] = df[columns].apply(lambda x: x.to_json(), axis=1)

with open('./config.json') as f:
  config = json.load(f)

df = pd.read_csv(
  filepath_or_buffer='./rick.csv',
  # dtype=config['headers']
)

for output in config['outputs']:
  if (output['type'] == 'map'):
    map(df, output['in_column'], output['out_column'], output['map'], output['default'])
  elif (output['type'] == 'math'):
    math(df, output['in_value_1'], output['in_value_2'], output['out_column'], output['operator'])
  elif (output['type'] == 'int'):
    convert_int(df, output['in_column'], output['out_column'])
  elif (output['type'] == 'rename'):
    df[output['out_column']] = df[output['in_column']]
  elif (output['type'] == 'meta'):
    meta(df, output['columns'])

print(df)
