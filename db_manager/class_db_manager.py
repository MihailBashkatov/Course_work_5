import psycopg2

from script.config import config, db_name


class DBManager:
    """ Class is aimed to perform SQL instructions"""

    def __init__(self, db_name: str):

        self.db_name: str = db_name

    def connect_to_database(self, instruction: str, word=None):

        # Parameters configuration
        params = config()

        # Adding to params new SQL database
        params['dbname'] = db_name

        try:
            # Connection to new database
            with psycopg2.connect(**params) as conn:
                # Creating cursor
                with conn.cursor() as cur:

                    # Execute instructions upon user's choice
                    if instruction == '1':
                        self.get_all_vacancies(cur)
                    elif instruction == '2':
                        self.get_companies_and_vacancies_count(cur)
                    elif instruction == '3':
                        self.get_avg_salary_per_vacancy(cur)
                    elif instruction == '4':
                        self.get_vacancies_with_higher_salary(cur)
                    elif instruction == '5':
                        self.get_vacancies_with_keyword(cur, word)

        except(Exception, psycopg2.DatabaseError) as error:
            print(error)

        finally:
            if conn is not None:
                conn.close()

    @staticmethod
    def get_companies_and_vacancies_count(cur) -> None:
        """  Get all employers list and amount their vacancies """

        cur.execute("""SELECT employer_name, COUNT(*) from vacancies
                       JOIN employers USING(employer_id)
                       GROUP BY employer_name""")

        query_result: tuple = cur.fetchall()
        for query in query_result:
            print(f'Employer: {query[0]}, vacancies: {query[1]}')

    @staticmethod
    def get_all_vacancies(cur) -> None:
        """ Get all vacancies list with their details  """

        cur.execute("""SELECT vacancies.name, employer_name, salary_from, salary_to, vacancy_url
                       FROM vacancies
                       JOIN employers USING(employer_id)""")

        query_result: tuple = cur.fetchall()
        for query in query_result:

            # Converting query to list to be able to change values
            query: list = list(query)
            if query[2] == 0:
                query[2]: str = '<info is not available>'
            elif query[3] == 0:
                query[3]: str = '<info is not available>'
            print(f'Vacancy: {query[0]}\nEmployer: {query[1]}\nSalary from: {query[2]}\nSalary to: {query[3]}\n'
                  f'Link to the vacancy: {query[4]}\n')

    @staticmethod
    def get_avg_salary_per_vacancy(cur) -> None:
        """ Get average salary per vacancy, if both: minimum and maximum salaries are presented"""

        cur.execute("""SELECT name, AVG((salary_to + salary_from) / 2) as average_salary
                       FROM vacancies
                       WHERE salary_from > 0 and salary_to > 0
                       GROUP BY vacancy_id""")

        query_result: tuple = cur.fetchall()
        for query in query_result:
            print(f'\nVacancy: {query[0]}, average salary: {round(query[1])}')
        print('***Please, note, that average salary is counted for vacancies, '
              f'where minimum and maximum levels are defined')

    @staticmethod
    def get_vacancies_with_higher_salary(cur) -> None:
        """ Get salary, which is above average level for all vacancies"""

        cur.execute(""" SELECT * , (SUM(salary_to)+SUM(salary_to))/2 as total_average_vacancy
                        FROM vacancies
                        WHERE salary_to > (SELECT (SUM(salary_to)+SUM(salary_to))/2
                        FROM vacancies 
                        WHERE salary_from > 0 and salary_to > 0)
                        GROUP BY vacancy_id""")

        query_result: tuple = cur.fetchall()
        if len(query_result) == 0:
            print('\nNo such vacancies\n')
        for query in query_result:
            print(f'Vacancy: {query[2]}\nCity: {query[3]}\nDescription: {query[4]}\n'
                  f'Salary from: {query[5]}\nSalary to: {query[6]}\n'
                  f'Link to the vacancy: {query[7]}\n')

    @staticmethod
    def get_vacancies_with_keyword(cur, word: str) -> None:
        """ Get salary for searched word"""

        cur.execute(f""" SELECT * 
                        FROM vacancies
                        WHERE name ILIKE '%{word}%' or description ILIKE '%{word}%'""")
        query_result: tuple = cur.fetchall()
        if len(query_result) == 0:
            print('\nNo such vacancies\n')

        for query in query_result:

            # Converting query to list to be able to change values
            query = list(query)
            if query[5] == 0:
                query[5]: str = '<info is not available>'
            elif query[6] == 0:
                query[6]: str = '<info is not available>'
            print(f'\nVacancy: {query[2]}\nCity: {query[3]}\nDescription: {query[4]}\n'
                  f'Salary from: {query[5]}\nSalary to: {query[6]}\n'
                  f'Link to the vacancy: {query[7]}\n')
