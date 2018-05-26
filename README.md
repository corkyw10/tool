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
 * Type `vagrant init ubuntu/trusty64` to tell Vagrant what kind of Linux VM you want to run
 * Run the virtual machine by running `vagrant up`and `vagrant ssh` to log in.
 * To load the data `cd` into  the newsdata file and use the command `psql -d news -f newsdata.sql`

If you get an error message saying:
  ```psql: FATAL: database "news" does not exist```
  ```psql: could not connect to server: Connection refused```
This means the database server isn't running or isn't set up correctly, you may need to download the
virual machine again into a fresh directory.
  
## Views required

In order to answer these questions it is neccessary to build the following views in the database

Run `psql news` in the command line

Paste the following code to create the necessary views:

  * ```
    create view top_three as
    select path, count(*) as num
    from log where path like '%article%'
    group by path
    order by num desc
    limit 3;
    ```
  * ```
    create view author_titles as
    select authors.name, articles.title, articles.slug
    from articles join authors
    on authors.id = articles.author
    order by name;
    ```
  * ```
    create view article_count as
    select path, count(*) as num
    from log where path like '%article%'
    group by path;
    ```
  * ```
    create view requests_made as
    select date_trunc('day', time), count(*) as num_requests
    from log
    group by date_trunc('day', time);
    ```
  * ```
    create view request_errors as
    select date_trunc('day', time), status, count(*) as num_errors
    from log where status != '200 OK'
    group by date_trunc('day', time), status
    order by date_trunc('day', time);
    ```
  * ```
    create view error_comparisons as
    select to_char(requests_made.date_trunc, 'FMMonth DD, YYYY'), 
    round(cast(num_errors as numeric)/num_requests*100),2) as percentage
    from request_errors join requests_made
    on request_errors.date_trunc = requests_made.date_trunc;
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
  

