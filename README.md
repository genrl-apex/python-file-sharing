# Python local file hosting system

## A python based file hosting system that lets you store html/php files then serve them using python

# !!! Not fully working yet

### Database<br>
- I would recommend using a <a href="http://mysql.com/" target="_blank">MySql</a> database as that is what i have been using
How to create/Structure<br>
- Make sure you have a running installation of your chosen database
- Create a database with the relevant command for your sql database service
- Then create a table using the command bellow (may not work with other sql database types)

CREATE TABLE files (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    description VARCHAR(255),
    file LONGBLOB NOT NULL,
    file_type VARCHAR(50) NOT NULL,
    hostable INT DEFAULT 0
);

- name should be the name of the file you are saving
- description should be a short description of the site
- file would be the file you choose
- file_type will be done worked out by the program
- if the file is html hostable will be = 1

Once the database setup is complete change the port/other credentials in connect_db.py if needed