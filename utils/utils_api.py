import json

import requests


def get_all_employers(word: str) -> [dict]:
    """ Return list of dicts, includes all employers upon word for search"""

    # Defining entering data
    param: dict = {'text': word,
                   'page': 0,
                   'per_page': 100}

    # pulling info from Headhunter and transform it in json format
    request = requests.get('https://api.hh.ru/employers', param)

    data = request.content.decode()
    json_object: dict = json.loads(data)['items']
    return json_object


def print_message_employers(employers_list) -> None:
    """ Printing all employers, who do have open vacancies"""

    # If list of dicts is not empty
    if len(employers_list) > 0:

        # Setting id for employer, then it will be used by user to choose employer
        employer_id: int = 0
        for employer in employers_list:
            if employer["open_vacancies"] == 0:
                continue
            employer_id += 1
            print(f'{employer_id} Company name: {employer["name"]}\n   '
                  f'Amount of open vacancies: {employer["open_vacancies"]}\n')
    else:
        print('No employers are found')


def get_employer(employer: str, employers_list: [dict]) -> [dict]:
    """ Return vacancies for chosen Employer. If no such Employer, return message"""

    # Defining entering data
    param = {'page': 0,
             'per_page': 100}

    # Set empty list, where employers with open vacancies will be added
    final_employers_list: list = []

    for chosen_employer in employers_list:
        if chosen_employer["open_vacancies"] != 0:
            final_employers_list.append(chosen_employer)

    # pulling info from Headhunter and transform it in json format
    # Request is performed by index in final_employers_list, 'employer' is a value, set by user
    request = requests.get(final_employers_list[int(employer) - 1]["vacancies_url"], param)
    data = request.content.decode()
    json_object: dict = json.loads(data)
    return json_object['items']


def print_message_vacancies(chosen_employer: [dict]) -> None:
    """ Printing info about vacancies"""

    try:
        for vacancy in chosen_employer:
            if vacancy['salary'] is None:
                vacancy['salary'] = {'from': None, 'to': None}
            if vacancy['salary'].get('from') is None:
                vacancy["salary"]["from"] = "<info is not available>"
            if vacancy['salary'].get('to') is None:
                vacancy["salary"]["to"] = "<info is not available>"
            if vacancy['snippet'].get('responsibility') is None:
                vacancy['snippet']["responsibility"] = "<info is not available>"

            print(f'  Vacancy name: {vacancy["name"]}\n'
                  f'  Description: {vacancy["snippet"]["responsibility"]}\n'
                  f'  City: {vacancy["area"]["name"]}\n'
                  f'  Salary from: {vacancy["salary"]["from"]} to {vacancy["salary"]["to"]}\n')
    except TypeError:
        return None
