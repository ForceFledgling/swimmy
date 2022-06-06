<p align="center">
 <img src="https://user-images.githubusercontent.com/92352077/172070427-9e2e2519-e28f-4e81-ae86-5529de256622.png" alt=""/>
</p>

Software system for organizing the work of sports swimming pools, assembled on:

* FastAPI
  * SQLAlchemy
  * Alembic
  * Pydantic
* PostgreSQL
* Docker-compose


# Features

Instructor:
* can work no more and no less than a certain number of hours per week
* has preferred opening hours

Administrator:
* can create groups and assign an instructor there, while choosing
* information about the instructor's current employment and intersection of group time with desired, sortable (overloaded instructors should not be displayed)
* can change the instructor in the group

Visitor:
* can choose a group and enroll in it

Group:
* limited by the number of people
* limited by the number of men and women (depending on the size appropriate dressing room)


# ⚡Fast implementation

**Step 1:** Clone this repository
```bash
git clone https://github.com/pvenv/swimmy.git
```

**Step 2:** Create a .env file in the project's root directory and add the following variables.

* Note: you can use secret library to generate jwt_secret
```python
from secrets import token_urlsafe
token_urlsafe(32)
```
* Example for .env file:
```bash
#FASTAPI
SERVER_PORT='8000'
JWT_SECRET='123456789zxcvbnm'

#POSTGRESQL
POSTGRES_HOST='swimmy-db'
POSTGRES_DB='swimmy'
POSTGRES_USER='root'
POSTGRES_PASSWORD='toor'
```

**Step 3:** Running and usage the project:
```bash
    cd swimmy  # root project dir
    docker-compose up -d
```

### 🎉 Additionally:

* You can populate the example in the database with the script when starting this project.

```bash
    cd swimmy  # root project dir
    docker-compose down
    docker-compose -f docker-compose.data.yml up --build --force-recreate --no-deps -d
```
or run the script manually, inside the container
```bash
    root@c1788b7d6f1c:/fastapi# python example_data.py
```