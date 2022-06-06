import os
import random

import psycopg2


DB = {
    'HOST': os.environ.get("POSTGRES_HOST"),
    'DB': os.environ.get("POSTGRES_DB"),
    'USER': os.environ.get("POSTGRES_USER"),
    'PASSWORD': os.environ.get("POSTGRES_PASSWORD"),
}


def users(cur) -> None:
    cur.execute("TRUNCATE TABLE users CASCADE")
    cur.execute("ALTER SEQUENCE users_id_seq RESTART WITH 1")

    administrator_password = '$2b$12$St0ShHVdvzL94RBE3bYomeHbQW8gFgQU9NHIJqxJPaDyOTBmW4td6'
    instructor_password = '$2b$12$.laS94AWNSw0/RycM6ix0ecE5ADChHyOUozsiqHctBzMZIIQ9/AoK'
    cleint_password = '$2b$12$kB6/qFIlN1vF1U81ltaOSe9k90v0DaMxoNbmowzf1Y2ULl3cDFsJ6'

    def _create(name, password, role) -> None:
        cur.execute(f"INSERT INTO users (email,username,sex,role_name,password_hash) VALUES\
            ('{name}@example.com', '{name}', '{random.choice(['male', 'female'])}', '{role}', '{password}')")

    def administrators(count: int = 1) -> None:
        for i in range(1, count + 1):
            _create(f'administrator{i}', administrator_password, 'administrator')

    def instructors(count: int = 2) -> None:
        for i in range(1, count + 1):
            _create(f'instructor{i}', instructor_password, 'instructor')

    def clients(count: int) -> None:
        for i in range(1, count + 1):
            _create(f'client{i}', cleint_password, 'client')

    administrators()
    instructors()
    clients(clients_count)


def rooms(cur) -> None:
    cur.execute("TRUNCATE TABLE rooms")
    cur.execute("ALTER SEQUENCE rooms_id_seq RESTART WITH 1")
    cur.execute(
        f"INSERT INTO rooms (name,sex,capacity) VALUES \
            ('Мужская', 'male', '{room_capacity_male}'),\
            ('Женская', 'female', '{room_capacity_female}')\
        ",
    )


def groups(cur) -> None:

    def _groups() -> None:
        cur.execute("TRUNCATE TABLE groups CASCADE")
        cur.execute("ALTER SEQUENCE groups_id_seq RESTART WITH 1")
        cur.execute(
            f"INSERT INTO groups (name,description,places,max_mans,max_womans) VALUES \
                ('Дети_1_утро', '10-14 лет', '{room_capacity_male + room_capacity_female}', \
                    '{room_capacity_male}', '{room_capacity_female}'),\
                ('Дети_2_утро', '10-14 лет', '{room_capacity_male + room_capacity_female}', \
                    '{room_capacity_male}', '{room_capacity_female}'),\
                ('Дети_3_день', '10-14 лет', '{room_capacity_male + room_capacity_female}', \
                    '{room_capacity_male}', '{room_capacity_female}'),\
                ('Дети_4_день', '10-14 лет', '{room_capacity_male + room_capacity_female}', \
                    '{room_capacity_male}', '{room_capacity_female}'),\
                ('Взрослые_1_утро', '14+ лет', '{room_capacity_male + room_capacity_female}', \
                    '{room_capacity_male}', '{room_capacity_female}'),\
                ('Взрослые_2_утро', '14+ лет', '{room_capacity_male + room_capacity_female}', \
                    '{room_capacity_male}', '{room_capacity_female}'),\
                ('Взрослые_3_день', '14+ лет', '{room_capacity_male + room_capacity_female}', \
                    '{room_capacity_male}', '{room_capacity_female}'),\
                ('Взрослые_4_день', '14+ лет', '{room_capacity_male + room_capacity_female}', \
                    '{room_capacity_male}', '{room_capacity_female}')\
            ",
        )

    def _groups_instructors() -> None:
        cur.execute("TRUNCATE TABLE groups_instructors CASCADE")
        cur.execute("ALTER SEQUENCE groups_instructors_id_seq RESTART WITH 1")
        cur.execute(
            "INSERT INTO groups_instructors (group_id,instructor_id) VALUES \
                (1, 2),\
                (2, 2),\
                (5, 2),\
                (6, 2),\
                (3, 3),\
                (4, 3),\
                (7, 3),\
                (8, 3)\
            ",
        )

    def _get_user_sex(user_id: int) -> str:
        cur.execute(f"SELECT sex FROM users WHERE id={user_id}")
        sex = cur.fetchone()[0]
        return sex

    def _groups_members() -> None:
        cur.execute("TRUNCATE TABLE groups_members CASCADE")
        cur.execute("ALTER SEQUENCE groups_members_id_seq RESTART WITH 1")

        client_id_start = 4
        client_id_end = client_id_start + clients_count
        users_male = []
        users_female = []
        for user_id in range(client_id_start, client_id_end):
            sex = _get_user_sex(user_id)
            if sex == 'male':
                users_male.append(user_id)
            elif sex == 'female':
                users_female.append(user_id)

        for group_id in range(1, 9):

            if len(users_male) > 0:
                for _ in range(room_capacity_male):
                    for user_id in users_male:
                        cur.execute(
                            f"INSERT INTO groups_members (group_id,member_id,member_sex) VALUES \
                                ('{group_id}', '{user_id}', 'male')",
                        )
                        users_male.remove(user_id)
                        break
            if len(users_female) > 0:
                for _ in range(room_capacity_male):
                    for user_id in users_female:
                        cur.execute(
                            f"INSERT INTO groups_members (group_id,member_id,member_sex) VALUES \
                                ('{group_id}', '{user_id}', 'female')",
                        )
                        users_female.remove(user_id)
                        break

    _groups()
    _groups_instructors()
    _groups_members()


if __name__ == '__main__':
    con = psycopg2.connect(
        database=DB['DB'],
        user=DB['USER'],
        password=DB['PASSWORD'],
        host=DB['HOST'],
        port="5432",
    )

    room_capacity_male = 5
    room_capacity_female = 8
    clients_count = 50

    print("Database opened successfully")
    cur = con.cursor()

    rooms(cur)
    users(cur)
    groups(cur)

    con.commit()
    print("Record inserted successfully")

    con.close()
