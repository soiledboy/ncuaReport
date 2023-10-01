from google.cloud import bigquery
import os
from google.auth.transport import requests
import google.auth.transport.requests
import pandas as pd 

def getData(credit_union):
  os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/Users/soiledboy/dev/ncua1/hjs-376018-f51f6dec11c4.json"

  client = bigquery.Client()

  #Define your project ID, dataset ID, and table names
  project_id = 'hjs-367018'
  dataset_id = 'ncua_data'
  table1_name = 'fs220'
  table2_name = 'fs220A'
  table3_name = 'fs220D'

  # Define the query parameters
  cu_numbers = [credit_union]
  cycle_dates = ['2022-12-31 00:00:00 UTC','2021-12-31 00:00:00 UTC' , '2020-12-31 00:00:00 UTC','2019-12-31 00:00:00 UTC' ]

  # Build the query string
  query = f"""
  SELECT O.CU_NUMBER, O.CYCLE_DATE, O.ACCT_018, O.ACCT_025B, O.ACCT_010, A.ACCT_997, D.ACCT_891
  FROM `hjs-376018.ncua_data.fs220` AS O
  JOIN `hjs-376018.ncua_data.fs220A` AS A
    ON O.CU_NUMBER = A.CU_NUMBER AND O.CYCLE_DATE = A.CYCLE_DATE
  JOIN `ncua_data.fs220D` AS D
    ON O.CU_NUMBER = D.CU_NUMBER AND O.CYCLE_DATE = D.CYCLE_DATE
  WHERE O.CU_NUMBER IN ({", ".join([str(cu) for cu in cu_numbers])})
    AND O.CYCLE_DATE IN ({", ".join([f"'{date}'" for date in cycle_dates])})
  """

  # Run the query
  query_job = client.query(query)

  # Wait for the query to complete
  query_job.result()

  query_result = query_job.result()
  # Convert the query result to a DataFrame
  df = pd.DataFrame(data=[row.values() for row in query_result], columns=('CU_NUMBER','CYCLE_DATE','ACCT_018','ACCT_025B','ACCT_010','ACCT_997','ACCT_891'))

  # Display the DataFrame
  print(df)
  return df