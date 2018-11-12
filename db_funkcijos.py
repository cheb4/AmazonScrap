# duomenu bazes funkcijos
import pymysql

print("uzkrove db_funkcijos")


##################


def patikrinti_db(sql, login):
    """ pasiema sql komanta ir prisijungima prie db
    :returns tuple su ataskymu"""
    # amazon_db_login = {"host": "localhost", "user": "root", "password": "", "database": "amazon"}
    db = pymysql.connect(login["host"], login["user"], login["password"], login["database"])
    cursor = db.cursor()
    try:  # kad nieko nemestu
        cursor.execute(sql)
        atsakymas = cursor.fetchall()
    except:
        atsakymas = "nepavyko pagauti visu"
        print("grazinu db kaip buvo")
        # Rollback in case there is any error
        db.rollback()
    db.close()
    return atsakymas


def vygdyti_sql_uzklausa(sql, login):
    """ pasiema sql komanda ir prisijungima prie db ivygdo comanda"""
    # login pavizdys
    # amazon_db_login = {"host": "localhost", "user": "root", "password": "", "database": "amazon"}
    db = pymysql.connect(login["host"], login["user"], login["password"], login["database"])
    cursor = db.cursor()
    duomenys = sql.encode('utf-8')
    try:
        cursor.execute(duomenys)
        db.commit()
    except:
        print("--------\ngrazinu db kaip buvo sql uzklausa:\n {} \n--------".format(sql))
        # Rollback in case there is any error
        db.rollback()
    db.close()
    return



def sukurti_lentele_istrinti_sena(pavadinimas, login):
    """ sukuria lentele jeigu nera, istrina sena"""
    db = pymysql.connect(login["host"], login["user"], login["password"], login["database"])
    cursor = db.cursor()
    sql = """CREATE TABLE `{pavadinimas}` (
      `id` int(255) NOT NULL AUTO_INCREMENT PRIMARY KEY,
      `pavadinimas` varchar(999) NOT NULL,
      `kaina` float NOT NULL,
      `ivertinimas` float NOT NULL,
      `stars` int(255) NOT NULL,
      `prime` tinyint(1) NOT NULL,
      `foto` varchar(9999) NOT NULL,
      `link` varchar(9999) NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8;""".format(pavadinimas=pavadinimas)
    try:
        cursor.execute(sql)
    except:
        print("nepavyko sukurti lenteles lenteles kurimo sql:\n {} ".format(sql))
        print("bandau istrinti sena db")
        try:
            cursor.execute("DROP TABLE IF EXISTS {}".format(pavadinimas))
            print("istryne sena lentele {}".format(pavadinimas))
            try:
                print("bandau sukurti \n {} ".format(pavadinimas))
                cursor.execute(sql)
                print("pavyko sukurti")
            except:
                print("visiskai nepavyko sukurti lenteles lenteles kurimo sql:\n {} ".format(sql))
        except:
            print("ivyko klaida trinant sena lentele {}".format(pavadinimas))
            print("DROP TABLE IF EXISTS {}".format(pavadinimas))
    db.close()


def istrinti_lentele(pavadinimas, login):
    """ istrina sena"""
    db = pymysql.connect(login["host"], login["user"], login["password"], login["database"])
    cursor = db.cursor()
    try:
        cursor.execute("DROP TABLE IF EXISTS {}".format(pavadinimas))
        print("istryne sena lentele {}".format(pavadinimas))
    except:
        print("---------\nivyko klaida trinant sena lentele: {}".format(pavadinimas))
        print("DROP TABLE IF EXISTS {}\n---------".format(pavadinimas))
    db.close()

def sukurti_lentele(pavadinimas, login):
    """ sukuria lentele"""
    # amazon_db_login = {"host": "localhost", "user": "root", "password": "", "database": "amazon"}
    db = pymysql.connect(login["host"], login["user"], login["password"], login["database"])
    cursor = db.cursor()
    sql = """CREATE TABLE `{pavadinimas}` (
  `id` int(255) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `pavadinimas` varchar(999) NOT NULL,
  `kategorija` varchar(999) NOT NULL,
  `kaina` float NOT NULL,
  `ivertinimas` float NOT NULL,
  `stars` int(255) NOT NULL,
  `prime` tinyint(1) NOT NULL,
  `foto` varchar(999) NOT NULL,
  `link` varchar(999) NOT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;""".format(pavadinimas=pavadinimas)
    try:  # kad nieko nemestu
        cursor.execute(sql)
        db.commit()
        print("sukure lentele: {}".format(pavadinimas))
    except:
        print("------\nnepavyko sukurti lenteles lenteles kurimo sql:\n {} \n------ grazinu kaip buvo".format(sql))
        db.rollback()
    db.close()

def parodyti_lenteles_db(login):
    """ :returns visos lenteles kurios yra db"""
    # amazon_db_login = {"host": "localhost", "user": "root", "password": "", "database": "amazon"}
    db = pymysql.connect(login["host"], login["user"], login["password"], login["database"])
    cursor = db.cursor()
    sql = """SHOW TABLES IN `{}`;""".format(login["database"])
    try:  # kad nieko nemestu
        cursor.execute(sql)
        lenteles = cursor.fetchall()
    except:
        print("nepavyko sukurti lenteles lenteles kurimo sql:\n {} ".format(sql))
        lenteles = "nera lenteliu"
    db.close()
    return lenteles


