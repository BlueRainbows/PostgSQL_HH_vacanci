from ClassM import HeadHunter, DBManager

if __name__ == '__main__':
    print('Программа обрабатывает поиск вакансий, ожидайте')
    hh = HeadHunter(['881164', '3772565', '653947', '1272486', '9052262',
                     '924205', '30637', '2222250', '2870783', '9694561'])
    hh_vacancy = hh.get_api()

    while True:
        try:
            user_request = int(input(
                """Вы можете выбрать следующие параметры:
1 - Получить список всех компаний и количество вакансий у каждой компании.
2 - Получить список всех вакансий с указанием названия компании,
названия вакансии, зарплаты и ссылки на вакансию
3 - Получить среднюю зарплату по вакансиям
4 - Получить список всех вакансий, у которых зарплата выше средней по всем вакансиям
5 - Получить список вакансий по ключевому слову.

0 - Для выхода из программы.
"""
            ))
            databases = DBManager(hh_vacancy)
            databases.get_connect_database()
            if user_request == 1:
                data_1 = databases.get_companies_and_vacancies_count()
                for data in data_1:
                    print(*data)
            elif user_request == 2:
                data_2 = databases.get_all_vacancies()
                for data in data_2:
                    print(*data)
            elif user_request == 3:
                data_3 = databases.get_avg_salary()
                for data in data_3:
                    print(*data)
            elif user_request == 4:
                data_4 = databases.get_vacancies_with_higher_salary()
                for data in data_4:
                    print(*data)
            elif user_request == 5:
                keyword = input('Введите слово для поискового запроса: ').lower()
                databases = DBManager(hh_vacancy, keyword)
                data_5 = databases.get_vacancies_with_keyword()
                for data in data_5:
                    print(*data)
            elif user_request == 0:
                break
            else:
                print('Параметр не найден')
        except ValueError:
            print('\nВведите число')
