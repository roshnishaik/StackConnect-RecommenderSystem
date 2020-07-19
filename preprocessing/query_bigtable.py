from google.cloud import bigquery

import queries as query
#os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 

client = bigquery.Client()

def get_max_views():
    query_job = client.query(query.max_views)
    df = query_job.to_dataframe()
    return df

def get_tags():
    query_job = client.query(query.wordcloud_tags)
    df = query_job.to_dataframe()
    return df

query_job = client.query(query.tag_clean)
df = query_job.to_dataframe()
df.to_csv('tags.csv')  

#results = query_job.result()  # Waits for job to complete.

#for row in results:
#    print("{} : {} views".format(row.url, row.view_count))