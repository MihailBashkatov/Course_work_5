from db_manager.class_db_manager import DBManager
from script.config import config, db_name
from utils.utils_api import get_all_employers, print_message_employers, get_employer, print_message_vacancies
from utils.utils_database import create_database, execute_tables


def get_vacancies():
    """ Main script is performing users' logic. It contains several steps for user's choice """
    while True:
        # Insert a word for search employers
        word: str = input('Insert a word, describing your interest. To quit insert [0]\n')
        if word == '0':
            print('Search is over')
            quit()

        # Getting list of dicts of employers according to inserted word
        employers_list: [dict] = get_all_employers(word)

        # Printing employers with open vacancies
        print_message_employers(employers_list)

        # If no employers are found with open vacancies, return to the start
        if len(employers_list) == 0:
            continue

        # Option for user to continue with particular Employer or return to the start
        response: word = input('To see particular Employer, press [1]. '
                               'To return to search mode, press [any other key]. '
                               'To quit insert [0]\n')

        if response == '1':
            chosen_employer = ''
            while True:
                # User is choosing which Employer shall be chosen
                employer = input('Insert number of employer, describing your interest\n')
                try:
                    # Creating a list of dicts with open vacancies
                    chosen_employer = get_employer(employer, employers_list)
                    break
                except IndexError:
                    print('\nInserted value does not correspond with Employers id. Try again.\n')
                    continue
                except ValueError:
                    print('\nInserted value is not digit. Try again\n')
                    continue

            # Printing all open vacancies
            print_message_vacancies(chosen_employer)
        elif response == '0':
            print('Search is over')
            quit()
        else:
            continue

        # Option to save searched vacancies
        if_save: str = input('If want to save vacancies, press [1]. '
                             'To return search mode, press [any other key] [any other key], '
                             'To quit insert [0]\n')
        if if_save == '0':
            print('Search is over')
            quit()
        elif if_save == '1':

            # Config parameters
            params = config()

            # Creating SQL database
            create_database(params=params, db_name=db_name)

            # Adding to params new SQL database
            params['dbname'] = db_name

            # Populating SQL database
            execute_tables(params, chosen_employer)
            print('Vacancies are saved in database')
        else:
            continue

        while True:

            # Option for user to choose option for search from SQL table
            instruction = input('\nIf want to see all saved vacancies, press [1].\n'
                                'If want to see count of employers and vacancies, press [2].\n'
                                'If want to see average salary per vacancy, press [3].\n'
                                'If want to see vacancies above total average salary, press [4].\n'
                                'If want to search vacancy, press [5].\n'
                                'To return search mode, press [any other key],\n'
                                'To quit insert [0]\n')

            # Creating object of class DBManager
            data_base_instruction = DBManager(db_name)
            if instruction == '0':
                print('\nSearch is over')
                quit()

            # Performing instruction in case user chose either or 1234
            elif instruction in '1234':
                data_base_instruction.connect_to_database(instruction)
                continue

            # Performing instruction in case user chose 5, where word will be needed
            elif instruction == '5':

                # Word for search
                searched_word: str = input('Please, type what you search\n').strip().lower()
                data_base_instruction.connect_to_database(instruction, searched_word)
                continue
            else:
                break
