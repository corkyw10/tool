# Logs analysis reporting tool

This is a python reporting tool for the Udacity logs analysis project.  

The purpose of the project is to use `psycopg2` to query a mock PostgreSQL database for a fictional news website. 

### What the tool does

The tool answers three questions:
  1. What are the most popular three articles of all time?
  2. Who are the most popular article authors of all time?
  3. On which days did more than 1% of requests lead to errors?
  
### Database tables

The database has three tables:
  * `authors` includes information about the authors of articles
  * `articles` includes the articles themselves
  * `log` includes one entry for each time a user has accessed the site
  
## Running the program

The program is designed to be run via the Udacity linux virtual machine command line.

You can install VirtualBox via this [link](https://www.virtualbox.org/wiki/Downloads) and vagrant, the command line utility to manage the virtual machine [here](https://www.vagrantup.com/downloads.html). 
  
 * Create a folder to store the files for this project and then open the folder with the terminal.
 * newsdata.zip contains the newsdata.sql database structure, save this, create_views.sql and tool.py in your project folder.
 * Save Vagrantfile in your vagrant folder.
 * Type `vagrant init ubuntu/trusty64` to tell Vagrant what kind of Linux VM you want to run
 * Run the virtual machine by running `vagrant up`and `vagrant ssh` to log in.
 * To load the data `cd` into  the project folder and use the command `psql -d news -f newsdata.sql`
 * To load the views required to run the program run the command `psql -d news -f create_views.sql` 

If you get an error message saying:
 - ```psql: FATAL: database "news" does not exist```
 - ```psql: could not connect to server: Connection refused```
 
This means the database server isn't running or isn't set up correctly, you may need to [download](https://github.com/udacity/fullstack-nanodegree-vm) the
virual machine again into a fresh directory.
  
## Views required

The views required to run the program can be imported from create_views.sql for ease of use.

The views are as follows:

```sql
CREATE VIEW top_three AS
     SELECT path, count(*) AS num
       FROM log 
      WHERE path LIKE '%article%'
   GROUP BY path
   ORDER BY num DESC
      LIMIT 3;

CREATE VIEW author_titles AS
     SELECT authors.name, articles.title, articles.slug
       FROM articles 
            JOIN authors
            ON authors.id = articles.author
   ORDER BY name;

CREATE VIEW article_count AS
     SELECT path, count(*) AS num
       FROM log 
      WHERE path LIKE '%article%'
   GROUP BY path;

CREATE VIEW requests_made AS
     SELECT date_trunc('day', time), count(*) AS num_requests
       FROM log
   GROUP BY date_trunc('day', time);

CREATE VIEW request_errors AS
     SELECT date_trunc('day', time), status, count(*) AS num_errors
       FROM log 
      WHERE status != '200 OK'
   GROUP BY date_trunc('day', time), status
   ORDER BY date_trunc('day', time);

CREATE VIEW error_comparisons AS
     SELECT to_char(requests_made.date_trunc, 'FMMonth DD, YYYY'), 
            round(cast(num_errors AS numeric)/num_requests*100,2) AS percentage
       FROM request_errors 
            JOIN requests_made
            ON request_errors.date_trunc = requests_made.date_trunc;
```


    
## Run program

To run the program run `python tool.py` in the command line

## Output

A plain text example of what is returned by the tool program can be seen in results.txt

## References

* https://www.postgresql.org/docs/
* https://docs.python.org/3/contents.html
* https://pyformat.info/
* https://discussions.udacity.com/t/understanding-how-to-create-the-logs-analysis-project-reporting-tool/367472/7
  

