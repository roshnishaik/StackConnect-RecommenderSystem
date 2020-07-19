max_views = """
    SELECT
      CONCAT(
        'https://stackoverflow.com/questions/',
        CAST(id as STRING)) as url,
      view_count
    FROM `bigquery-public-data.stackoverflow.posts_questions`
    WHERE tags like '%google-bigquery%'
    ORDER BY view_count DESC
    LIMIT 10"""

wordcloud_tags = """SELECT tags
         FROM `bigquery-public-data.stackoverflow.posts_questions`
         LIMIT 200000;
         """ 

tag_clean = """ SELECT title,body,tags,score 
			FROM `bigquery-public-data.stackoverflow.stackoverflow_posts` 
			LIMIT 5000"""   