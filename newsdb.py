# "Database code" for the newspaper statistics.

# import datetime
import psycopg2
DBNAME = "news"


def top_three():
    """Return top 3 popular articles by desc order"""
    try:
        db = psycopg2.connect(database=DBNAME)
    except psycopg2.Error as e:
        print "Unable to connect!"
        print e.pgerror
        print e.diag.message_detail
        sys.exit(1)
    else:
        print "Connected!"
    c = db.cursor()
    c.execute(
                    "select a.title, subq.num from articles as a join "
                    "(select path, count(*) as num from log join articles "
                    "on log.path = '/article/' || articles.slug "
                    "group by path order by num desc limit 3) "
                    "as subq on subq.path = '/article/'|| a.slug "
                    "order by num desc; "
                    )
    top_three = c.fetchall()
    db.close()
    return top_three


def popular_author():
    """Return popular author of all time"""
    try:
        db = psycopg2.connect(database=DBNAME)
    except psycopg2.Error as e:
        print "Unable to connect!"
        print e.pgerror
        print e.diag.message_detail
        sys.exit(1)
    else:
        print "Connected!"
    c = db.cursor()
    c.execute(
                    "select auth.name,sum(subq2.num) "
                    "as total from authors as auth join "
                    "(select a.author,a.title,subq.num from articles "
                    "as a join "
                    "(select path,count(*) as num from log join articles "
                    "on path = '/article/'|| articles.slug group by path "
                    "order by num desc) "
                    "as subq on subq.path = '/article/'|| a.slug "
                    "order by num desc) "
                    "as subq2 on subq2.author=auth.id group by auth.id; "
                    )
    popular_author = c.fetchall()
    db.close()
    return popular_author


def bug_percentile():
    """Return bug percentage >1"""
    try:
        db = psycopg2.connect(database=DBNAME)
    except psycopg2.Error as e:
        print "Unable to connect!"
        print e.pgerror
        print e.diag.message_detail
        sys.exit(1)
    else:
        print "Connected!"
    c = db.cursor()
    c.execute(
                    "select * from (select subq.date_by_day, "
                    "(cast(subq.bugs as decimal)/subq.total_logs *100) "
                    "as bug_p from (select date_trunc('day',time) "
                    "as date_by_day, count(*) as total_logs, "
                    "count(*) filter (where status!='200 OK') as bugs "
                    "from log group by date_by_day) "
                    "as subq) "
                    "as subq2 where subq2.bug_p>1;"
                    )
    bugs = c.fetchall()
    db.close()
    return bugs
