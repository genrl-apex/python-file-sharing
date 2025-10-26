# Python file sharing system

## A file sharing system that lets you store files then share/serve them using python

### About this project

this project is a python based app that reads from and displays files from a database that can then be previewed, downloaded and in some cases hosted on localhost. this is a great way to share files between friends, family or even a work environment


### Installation
---

> **Notice**
> You will need to setup your own database, specifically a MySql one so if you haven't already install the latest community version from their [`website`](http://mysql.com/)

#### Method 1: included file

run db_setup.sql to quickly setup the database
[`db_setup.sql`](./db_setup.sql)


#### Method 2: setup directly with statement

```bash
CREATE TABLE files (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    description VARCHAR(255),
    file LONGBLOB NOT NULL,
    file_type VARCHAR(50) NOT NULL,
    hostable INT DEFAULT 0
);
```