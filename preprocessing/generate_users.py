from google.cloud import bigquery
import queries as query

client = bigquery.Client()
query_job = client.query(query.max_views)
df = query_job.to_dataframe()