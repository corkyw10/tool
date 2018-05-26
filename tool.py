#!/usr/bin/env python2
# database code for newsdata

import psycopg2

DBNAME = "news"


def connect(query):
	"""Connect to database and run query."""
    conn = psycopg2.connect(database=DBNAME)
    c = conn.cursor()
    c.execute(query)
    results = c.fetchall()
    conn.close()
    return results


def top_three():
	"""Return top three articles and how many views they have in descending order."""
    results = connect("""select title, num from articles, top_three
        where top_three.path = concat('/article/',articles.slug)
        order by num desc;""")
    print 'The top three articles are:'
    print '---'
    for result in results:
        print '"{}" -- {} views'.format(result[0], result[1])
    print '---'


def top_authors():
	"""Return authors in order of most popular to least popular."""
    results = connect("""select author_titles.name, sum(article_count.num)
        from author_titles, article_count
        where article_count.path like concat('/article/',author_titles.slug)
        group by author_titles.name
        order by sum desc;""")
    print 'The most popular authors are:'
    print '---'
    for result in results:
        print '{} -- {} views'.format(result[0], result[1])
    print '---'


def high_error_days():
	"""Return days on which over 1% of requests resulted in errors and 
	percentage of errors there were.
	"""
    results = connect("""select * from error_comparisons
        where percentage > 1;""")
    print 'Dates when errors higher than 1%:'
    print '---'
    for result in results:
        print '{} -- {}% errors'.format(result[0], result[1])
    print '---'


if __name__ == '__main__':
	"""Print results of all three queries."""
    top_three()
    top_authors()
    high_error_days()
