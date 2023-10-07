import psycopg2


def create_database(params: dict, db_name: str) -> None:
    """ Create SQL database """

    # Creating connection to postgres
    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    # Checking if database already exists. If not, then database creating
    cur.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (db_name,))
    exists = cur.fetchone()
    if not exists:
        cur.execute(f"CREATE DATABASE {db_name}")

    conn.close()


def check_table_exists(cur, table_name: str):
    """ # Checking if table already exists. If not, then database creating"""

    cur.execute("SELECT EXISTS (SELECT FROM pg_tables WHERE tablename='%s')" % table_name)
    result = cur.fetchone()[0]

    return result


def create_employers_table(cur) -> None:
    """Create a table employers"""

    # Check if table employers is already existed
    check_table = check_table_exists(cur, 'employers')
    if check_table:
        return None

    # If table does not exist, it is created
    cur.execute("""
                    CREATE TABLE employers
                        (
                        employer_id INTEGER PRIMARY KEY,
                        employer_name VARCHAR(100) NOT NULL
                        )
                """
                )


def insert_employers_data(cur, chosen_employer: list[dict]) -> None:
    """ Populating data to table employers from list of dicts."""

    employer_id: str = chosen_employer[0]['employer']['id']
    employer_name: str = chosen_employer[0]['employer']['name']

    cur.execute(""" INSERT INTO employers (employer_id, employer_name)
                VALUES (%s, %s)  ON CONFLICT (employer_id) DO NOTHING""", # if employer with id already exists, continue
                (employer_id, employer_name))


def create_vacancies_table(cur) -> None:
    """Create a table vacancies"""

    # Check if table vacancies is already existed
    check_table = check_table_exists(cur, 'vacancies')
    if check_table:
        return None

    # If table does not exist, it is created
    cur.execute("""
                     CREATE TABLE vacancies
                         (
                          vacancy_id INTEGER PRIMARY KEY,
                          employer_id INTEGER NOT NULL,
                          name VARCHAR(255) NOT NULL,
                          city VARCHAR(100) NOT NULL,
                          description TEXT,
                          salary_from INTEGER,
                          salary_to INTEGER,
                          vacancy_url TEXT,

                          CONSTRAINT fk_vacancies_employer_id FOREIGN KEY(employer_id) REFERENCES employers(employer_id)
                         )
                      """
                )


def insert_vacancies_data(cur, chosen_employer: list[dict]) -> None:
    """ Populating data to table vacancies from list of dicts."""

    for vacancy in chosen_employer:
        vacancy_id: str = vacancy['id']
        employer_id: str = vacancy['employer']['id']
        name: str = vacancy["name"]
        city: str = vacancy["area"]["name"]
        description: str = vacancy["snippet"]["responsibility"]
        salary_from: int = vacancy["salary"]["from"]

        # Converting salary value to integer
        if type(salary_from) == str:
            salary_from: int = 0
        salary_to: int = vacancy["salary"]["to"]
        if type(salary_to) == str:
            salary_to: int = 0
        vacancy_url: str = vacancy['alternate_url']

        cur.execute(""" INSERT INTO vacancies 
                            (
                             vacancy_id,
                             employer_id,
                             name, 
                             city,
                             description,
                             salary_from,
                             salary_to,
                             vacancy_url
                             )
                            VALUES 
                            (
                             %s, %s, %s, %s, %s, %s, %s, %s
                             )  ON CONFLICT (vacancy_id) DO NOTHING                         
                         """,  # if employer with id already exists, continue
                    (
                        vacancy_id, employer_id, name, city, description, salary_from, salary_to, vacancy_url
                    )
                    )


def execute_tables(params, chosen_employer) -> None:
    """ Execute creating and populating tables"""
    try:
        # Connection to new database
        with psycopg2.connect(**params) as conn:

            # Creating cursor
            with conn.cursor() as cur:

                # Create and populate tables employers and vacancies
                create_employers_table(cur)
                insert_employers_data(cur, chosen_employer)
                create_vacancies_table(cur)
                insert_vacancies_data(cur, chosen_employer)

    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
