# "Database code" for the DB Forum.

# import datetime
import psycopg2
DBNAME = "news"

def top_three():
    """Return top 3 popular articles by desc order"""
    db = psycopg2.connect(database=DBNAME);
    c = db.cursor();
    c.execute("select a.title,subq.num from articles as a join (select path,count(*) as num from log where path like '%/article/%' group by path order by num desc limit 3) as subq on subq.path like '%'||a.slug||'%' order by num desc;");
    top_three = c.fetchall();
    db.close();
    return top_three;


def popular_author():
    """Return popular author of all time"""
    db = psycopg2.connect(database=DBNAME);
    c = db.cursor();
    c.execute("select auth.name,sum(subq2.num) as total from authors as auth join (select a.author,a.title,subq.num from articles as a join (select path,count(*) as num from log where path like '%/article/%' group by path order by num desc) as subq on subq.path like '%'||a.slug||'%' order by num desc) as subq2 on subq2.author=auth.id group by auth.id;");
    popular_author = c.fetchall();
    db.close();
    return popular_author;

def bug_percentile():
    """Return bug percentage >1"""
    db = psycopg2.connect(database=DBNAME);
    c = db.cursor();
    c.execute("select * from (select subq.date_by_day, (cast(subq.bugs as decimal)/subq.total_logs *100) as bug_p from (select date_trunc('day',time) as date_by_day, count(*) as total_logs, count(*) filter (where status!='200 OK') as bugs from log group by date_by_day) as subq) as subq2 where subq2.bug_p>1;");
    bugs = c.fetchall();
    db.close();
    return bugs;

def get_posts():
  """Return all posts from the 'database', most recent first."""
  db = psycopg2.connect(database=DBNAME);
  c = db.cursor();
  c.execute("select content, time from posts order by time desc");
  posts = c.fetchall();
  db.close();
  return posts

def add_post(content):
  """Add a post to the 'database' with the current timestamp."""
  db = psycopg2.connect(database=DBNAME)
  c = db.cursor();
  c.execute("insert into posts values (%s)", (content,));
  db.commit();
  db.close();
  # POSTS.append((content, datetime.datetime.now()))
# select path,count(*) as num from log where path!='/' group by path order by num desc limit 3;
 # select a.title, b.num from articles as a join top_three as b on b.path like '%'||a.slug||'%' order by num desc;
 # select path, count(*) from log group by path; find author by joining with articles (to find author id); join with articles and aggregate by grouping articles.aurthor(id), order by num desc
 #group log by date, count the # of each days, then divide by # of erros for each day, then filter out >=1% error dates;
 #finally modify the html template to display the information on the web app
 #write the readme file;

# select auth.name,auth.id,sum(subq2.num) as total from authors as auth join (select a.author,a.title,subq.num from articles as a join (select path,count(*) as num from log where path like '%/article/%' group by path order by num desc) as subq on subq.path like '%'||a.slug||'%' order by num desc) as subq2 on subq2.author=auth.id group by auth.id;
# select * from (select subq.date_by_day, (cast(subq.bugs as decimal)/subq.total_logs *100) as bug_p from (select date_trunc('day',time) as date_by_day, count(*) as total_logs, count(*) filter (where status!='200 OK') as bugs from log group by date_by_day) as subq) as subq2 where subq2.bug_p>1;
