import requests
import os
import psycopg2
import json


class HeadHunter:
    """ Класс для получения API сайта HeadHunter """
    url = 'https://api.hh.ru/vacancies'

    def __init__(self, id_company):
        self.id_company = id_company

    def get_api(self):
        try:
            list_vacancy = []
            with (open('company_file.json', 'w', encoding='utf-8') as file):
                for company in self.id_company:
                    response_hh = requests.get(url=self.url, headers={'User-Agent': 'bluereinbow@yandex.ru'},
                                               params={'page': None, 'per_page': 20, 'employer_id': company})
                    for item in response_hh.json()['items']:
                        company_id = item['employer']['id']
                        company_name = item['employer']['name']
                        company_url = item['employer']['alternate_url']
                        vacancy_name = item['name']
                        vacancy_city = item['area']['name']
                        if item['salary'] is None:
                            vacancy_salary_from = 0
                            vacancy_salary_to = 0
                        else:
                            salary_from = item['salary']['from']
                            if salary_from is None:
                                vacancy_salary_from = 0
                            else:
                                vacancy_salary_from = salary_from
                            salary_to = item['salary']['to']
                            if salary_to is None:
                                vacancy_salary_to = 0
                            else:
                                vacancy_salary_to = salary_to
                        vacancy_url = item['alternate_url']
                        dict_vacancy = {
                            'company_id': company_id,
                            'company_name': company_name,
                            'company_url': company_url,
                            'vacancy_name': vacancy_name,
                            'vacancy_city': vacancy_city,
                            'vacancy_salary_from': vacancy_salary_from,
                            'vacancy_salary_to': vacancy_salary_to,
                            'vacancy_url': vacancy_url
                        }
                        list_vacancy.append(dict_vacancy)
                json.dump(list_vacancy, file, ensure_ascii=False, indent=4)
            with open('company_file.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
            return data
        except requests.RequestException as error:
            print(f'Возникла ошибка {error}')


class DBManager:
    """ Класс для работы с базой данных """

    def __init__(self, vacancy):
        self.vacancy = vacancy

    def get_connect_database(self):
        """ Метод для создания базы данных """
        with psycopg2.connect(
                host="localhost",
                database="ProjVacancy",
                user="postgres",
                password=os.environ.get('PASSWORD_FOR_POSTGRESQL')
        ) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                CREATE TABLE IF NOT EXISTS company
                (
                    company_id int PRIMARY KEY,
                    company_name varchar(100) NOT NULL,
                    company_url varchar(100) NOT NULL
                );
                CREATE TABLE IF NOT EXISTS vacancy
                (
                    vacancy_id serial PRIMARY KEY,
                    vacancy_name varchar(100) NOT NULL,
                    vacancy_city varchar(100),
                    vacancy_salary_from int,
                    vacancy_salary_to int,
                    vacancy_url varchar(100) NOT NULL,
                    company_vacancy int REFERENCES company(company_id)
                )
                """)

                for data_vacancy in self.vacancy:
                    cur.execute('INSERT INTO company VALUES (%s, %s, %s) ON CONFLICT DO NOTHING',
                                (data_vacancy['company_id'],
                                 data_vacancy['company_name'],
                                 data_vacancy['company_url']))
                    cur.execute('INSERT INTO vacancy'
                                '(vacancy_name, vacancy_city, vacancy_salary_from, vacancy_salary_to, '
                                'vacancy_url, company_vacancy)'
                                ' VALUES (%s, %s, %s, %s, %s, %s)',
                                (data_vacancy['vacancy_name'],
                                 data_vacancy['vacancy_city'],
                                 data_vacancy['vacancy_salary_from'],
                                 data_vacancy['vacancy_salary_to'],
                                 data_vacancy['vacancy_url'],
                                 data_vacancy['company_id']))

    def get_companies_and_vacancies_count(self):
        """ получает список всех компаний и количество вакансий у каждой компании. """
        pass

    def get_all_vacancies(self):
        """ получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию. """
        pass

    def get_avg_salary(self):
        """ получает среднюю зарплату по вакансиям. """
        pass

    def get_vacancies_with_higher_salary(self):
        """ получает список всех вакансий, у которых зарплата выше средней по всем вакансиям. """
        pass

    def get_vacancies_with_keyword(self):
        """ получает список всех вакансий,
        в названии которых содержатся переданные в метод слова, например python."""
        pass
