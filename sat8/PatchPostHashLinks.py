from scrapy.conf import settings

from sat8.Helpers.Functions import *

conn = settings['MYSQL_CONN']
cursor = conn.cursor()

def saveHashLinks():
    queryPost = "SELECT * FROM posts"
    cursor.execute(queryPost)
    posts = cursor.fetchall()

    updated = 0
    for post in posts:
        # Update craw links
        sql = "REPLACE INTO post_hash_links(hash_link) VALUES(%s)"
        cursor.execute(sql, (md5(post['link'])))
        conn.commit()

        updated += 1

    print updated

saveHashLinks()