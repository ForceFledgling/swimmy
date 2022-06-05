from fastapi import FastAPI

from .api import router


tags_metadata = [
    {
        'name': 'auth',
        'description': 'Registration , authentication and authorization',
    },
    {
        'name': 'roles',
        'description': 'User role management',
    },
    {
        'name': 'instructors',
        'description': 'Instructor working hours',
    },
    {
        'name': 'rooms',
        'description': 'Working with dressing rooms',
    },
    {
        'name': 'groups',
        'description': 'Working with swimming groups',
    },
]


app = FastAPI(
    title='Swimmy',
    description='Web ARM for swimming pool',
    version='0.1.4',
    openapi_tags=tags_metadata,
)
app.include_router(router)
