# Swimmy

Software system for organizing the work of sports swimming pools.

### Infrastructure:
* FastAPI
  * SQLAlchemy
  * Alembic
* PostgreSQL
* Docker-compose

# Fast implementation

* Clone this repository
```bash
git clone https://github.com/pvenv/swimmy.git
```

* Create a .env file in the project's root directory and add the following variables.
```bash
#POSTGRESQL
POSTGRES_HOST='swimmy-db'
POSTGRES_DB='swimmy'
POSTGRES_USER='swimmy_db_username'
POSTGRES_PASSWORD='swimmy_db_passwrod'

# PG4ADMIN
PGADMIN_DEFAULT_EMAIL=admin
PGADMIN_DEFAULT_PASSWORD=admin
```

### Additionally:

* Fill in sample data via script at application start

```bash

```

# Features

Instructor:
* can work no more and no less than a certain number of hours per week;
* has preferred opening hours;

Administrator:
* can create groups and assign an instructor there, while choosing
* information about the instructor's current employment and intersection of group time with desired, sortable (overloaded instructors should not be displayed)
* can change the instructor in the group

Visitor:
* can choose a group and enroll in it

Group:
* limited by the number of people
* limited by the number of men and women (depending on the size appropriate dressing room)