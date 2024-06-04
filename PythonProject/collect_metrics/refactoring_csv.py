import csv
import logging
import numpy as np
import pandas as pd
logger = logging.getLogger(__name__)


column_times_names_to_refine = [
    "usage_usec",
    "user_usec",
    "system_usec"]
column_names_to_refine = [
    "nr_throttled",
    "throttled_usec",
    "rbytes",
    "wbytes",
    "rios",
    "wios",
    "workingset_refault_anon",
    "workingset_refault_file",
    "workingset_activate_anon",
    "workingset_activate_file",
    "workingset_restore_anon",
    "workingset_restore_file",
    "pgscan",
    "pgsteal",
    "pgscan_kswapd",
    "pgscan_direct",
    "pgsteal_kswapd",
    "pgsteal_direct",
    "pgfault",
    "pgmajfault",
    "pgrefill",
    "pgactivate",
    "rx_bytes",
    "tx_packets",
    "rx_packets",
    "tx_bytes",
]
column_names_to_remove = [
  "core_sched.force_idle_usec",
  "nr_bursts",
  "nr_periods",
  "burst_usec",
  "dbytes",
  "dios",
  "sec_pagetables",
  "zswap",
  "zswapped",
  "anon_thp",
  "file_thp",
  "shmem_thp",
  "unevictable",
  "workingset_nodereclaim",
  "pgscan_khugepaged",
  "pgsteal_khugepaged",
  "pgdeactivate",
  "pglazyfree",
  "pglazyfreed",
  "multicast",
  "zswpin",
  "zswpout",
  "thp_fault_alloc",
  "thp_collapse_alloc",
]


field_slab=[
  "slab_reclaimable",
  "slab_unreclaimable"
]
microsecond=1000000		

async def refactor(csv_filepath_input, csv_filepath_output, xls_filepath_output):
  logging.info("start refactoring")
  df = pd.read_csv(csv_filepath_input)
  logging.info("remove columns from csv")
  df=remove_columns(df,column_names_to_remove)
  logging.info("calculate delta of csv")
  df=calculate_deltas(df,column_times_names_to_refine)
  df=calculate_deltas(df,column_names_to_refine)
  df=calc_ratio_sec(df,column_names_to_refine,"usage_usec_delta")
  df=calc_ratio(df,field_slab,"slab")
  df.to_csv(csv_filepath_output, index=False)
  df.to_excel(xls_filepath_output)			


def calculate_deltas(df, column_names_to_refine):
  """
  Reads a CSV file, calculates deltas for specified columns between consecutive rows,
  and writes the results to a new CSV file using pandas.

  Args:
      df (pandas.DataFrame): Pandas dataframe of the csv file
      column_names_to_refine (list): List of column names for which deltas are to be calculated.
  Returns:
      pandas.DataFrame: The modified DataFrame without the removed columns.
  """
  for col in column_names_to_refine:
    #operate in one period 
    df[f"{col}_delta"] = df[col].diff(periods=1).fillna(0).astype(int)
    
  # Drop the original columns if not needed
  df =df.drop(columns=column_names_to_refine)
  return df
   



def remove_columns(df, columns_to_remove):
  """
  This function removes specified columns from a CSV file.

  Args:
      df (pandas.DataFrame:): Pandas dataframe of the csv file
      column_names_to_refine (list): List of column names for which deltas are to be calculated.

  Returns:
      pandas.DataFrame: The modified DataFrame without the removed columns.
  """

  # Remove the unwanted columns
  df = df.drop(columns=columns_to_remove)  # axis=1 specifies columns
  return df

def calc_ratio(df, column, field_divisor):
  for col in column:
    df[f"{col}_ratio"]=df[col]/df[field_divisor]
  df=df.drop(columns=column)
  return df

def calc_ratio_sec(df,data_column, time_column):
  for col in data_column:
   df[f"{col}/sec"]=df[f"{col}_delta"]/df[time_column]*microsecond
   df=df.drop(f"{col}_delta", axis=1)
  return df
"""
for file in ["/home/pietro/Documenti/unifi/magistrale/QAoS/Experimental_Analysis_of_Systems/QAS_Anomaly-Detection_on_health_system/PythonProject/output_csv/raw_20240426-201720.csv",
             "/home/pietro/Documenti/unifi/magistrale/QAoS/Experimental_Analysis_of_Systems/QAS_Anomaly-Detection_on_health_system/PythonProject/output_csv/raw_20240427-101704.csv",
             "/home/pietro/Documenti/unifi/magistrale/QAoS/Experimental_Analysis_of_Systems/QAS_Anomaly-Detection_on_health_system/PythonProject/output_csv/raw_20240427-105124.csv", 
             "/home/pietro/Documenti/unifi/magistrale/QAoS/Experimental_Analysis_of_Systems/QAS_Anomaly-Detection_on_health_system/PythonProject/output_csv/raw_20240427-112603.csv"]:
  df = pd.read_csv(file)
  logging.info("calculate delta of csv")
  df=remove_columns(df,column_names_to_remove)
  logging.info("calculate delta of csv")
  df=calculate_deltas(df,column_times_names_to_refine)
  df=calculate_deltas(df,column_names_to_refine)
  df=calc_ratio_sec(df,column_names_to_refine,"usage_usec_delta")
  df=calc_ratio(df,field_slab,"slab")
  df.to_excel(file+"_xls.xlsx")			"""