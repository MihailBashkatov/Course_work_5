The project is designed for searching vacancies in Headhunter.
The search is going via API under a word, inserted by user.
Search is split in several steps:
1) According to the word, Employers are searched
2) According to user's choice, particular employer is presented with all open vacancies
3) According to user's choice, vacancies are stored in sql table
4) According to user's choice, sql table is generating different results

There are 2 SQL tables: employees and vacancies. Both are connected via employee_id
Both tables are using id values, generated from HeadHunter

API logic, creating and populating database are performed via utils
SQL queries are performed via Class solution