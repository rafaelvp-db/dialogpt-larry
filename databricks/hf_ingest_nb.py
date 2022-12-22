# Databricks notebook source
!pip install pysub-parser

# COMMAND ----------

import glob
from zipfile import ZipFile

path = "/dbfs/FileStore/curbdata/"

for file in glob.glob(f"{path}/*.zip"):
  # Create a ZipFile Object and load sample.zip in it
  with ZipFile(file, 'r') as zip_file:
    # Extract all the contents of zip file in current directory
    zip_file.extractall(path=path)

# COMMAND ----------

!ls "/dbfs/FileStore/curbdata/"

# COMMAND ----------

from pysubparser import parser
from pysubparser.cleaners import ascii, brackets, formatting, lower_case
import pandas as pd


def subtitle_to_pandas(path: str):

  subtitles = parser.parse(path)

  subtitles = brackets.clean(
      lower_case.clean(
          subtitles
      )
  )
  
  dialog_list = []

  for subtitle in subtitles:
    record = {}
    record["start"] = subtitle.start
    record["end"] = subtitle.end
    record["text"] = subtitle.text
    record["id"] = subtitle.index
    dialog_list.append(record)
    
  result = pd.DataFrame.from_dict(dialog_list)
  
  return result

# COMMAND ----------

dataframe_list = []

for item in glob.glob(f"{path}/*.srt"):
  df = subtitle_to_pandas(item)
  dataframe_list.append(df)
  
full_df = pd.concat(dataframe_list, axis=0)

# COMMAND ----------

full_df.reset_index()

# COMMAND ----------

full_df["text"] = full_df.text.str.replace("- ", "")

# COMMAND ----------

full_df.head()

# COMMAND ----------

full_df.to_csv(f"{path}/curb_full.csv", sep="|")
