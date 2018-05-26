
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

