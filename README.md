# Swimmy

Software system for organizing the work of sports swimming pools.

### Infrastructure:
* FastAPI
  * SQLAlchemy
  * Alembic
  * Pydantic
* PostgreSQL
* Docker-compose

# Fast implementation

* Clone this repository
```bash
git clone https://github.com/pvenv/swimmy.git
```

* Create a .env file in the project's root directory and add the following variables.

Note: you can use secret library to generate jwt_secret
```python
from secrets import token_urlsafe
token_urlsafe(32)
```

```bash
#FASTAPI
SERVER_PORT='8000' 

#POSTGRESQL
POSTGRES_HOST='swimmy-db'
POSTGRES_DB='swimmy'
POSTGRES_USER='root'
POSTGRES_PASSWORD='toor'
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