#!/usr/bin/python3.6
# -*- coding: ascii -*-

# pagrindinis
from db_funkcijos import *
from amazonFun1 import *

amazon_db_login = {"host": "localhost", "user": "root", "password": "", "database": "amazon"}
amazon_products_db_login = {"host": "localhost", "user": "root", "password": "", "database": "amazon_prekes"}

proxies = {
    'http': 'http://190.152.4.54:65301',
    'https': 'http://137.74.168.174:8080',
}

viskas = patikrinti_db(sql="SELECT * FROM `nuorodos`", login=amazon_db_login)



for tuplas in viskas:
    # sukure lentele ir istryne sena jei buvo
    # sukurti_lentele_istrinti_sena(pavadinimas=tuplas[1], login=amazon_products_db_login)
    print("atsiunciu psl id: {}".format(tuplas[0]))
    # sukure db
    for y in range(3, 8):
        # tikrina ar url
        if len(tuplas[y]) < 5:
            continue
        # ties cia atsisiuncia psl
        gautas_masyvas = psl_scrap(url=tuplas[y], proxies=proxies)
        # # ties cia ideda i ideda i naujai sukurta lentele
        for uzklausa in gautas_masyvas:
            vygdyti_sql_uzklausa(sql=uzklausa.irasyti_i_db_lentele(lentele="visos", kategorija=tuplas[1]),
                                 login=amazon_products_db_login)

print("viskas atsiusta !!!")

vygdyti_sql_uzklausa(sql="""CREATE TABLE `Whitelist` (
  `id` int(255) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `pavadinimas` varchar(999) NOT NULL,
  `kategorija` varchar(999) NOT NULL,
  `kaina` float NOT NULL,
  `ivertinimas` float NOT NULL,
  `stars` int(255) NOT NULL,
  `prime` tinyint(1) NOT NULL,
  `foto` varchar(999) NOT NULL,
  `link` varchar(999) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
""", login=amazon_products_db_login)

# viska sudeti

vygdyti_sql_uzklausa(sql=""" insert INTO `Whitelist` (
     `pavadinimas`,
      `kategorija`,
      `kaina`,
       `ivertinimas`,
       `stars`,
       `prime`,
       `foto`,
       `link`
     )
    select
      `pavadinimas` as `pavadinimas`,
      `kategorija` as `kategorija`,
      `kaina` as `kaina`,
       `ivertinimas` as `ivertinimas`,
       `stars` as `stars`,
       `prime` as `prime`,
       `foto` as `foto`,
       `link` as `link`
 FROM `visos` WHERE kaina <= 25 and prime = 1 and  stars >= 20;""", login=amazon_products_db_login)

print("Viskas baigta ir atfiltruota")
