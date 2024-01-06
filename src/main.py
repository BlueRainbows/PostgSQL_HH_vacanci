from ClassM import HeadHunter, DBManager

if __name__ == '__main__':

    hh = HeadHunter(['881164', '3772565', '653947', '1272486', '9052262',
                    '924205', '30637', '2222250', '2870783', '9694561'])
    hh_vacancy = hh.get_api()

    databases = DBManager(hh_vacancy)
    databases.get_connect_database()


