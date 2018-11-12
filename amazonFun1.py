import requests
import bs4
import pymysql

# klase
print("uzkrove amazonFun1.py")


class preke():
    # pavadinimas str buna iki 300 char
    # kaina float list
    # ivertinimas float
    # stars int
    # prime bool
    # foto str ilgas
    # link str ilgas
    autoNr = 0

    def __init__(self, pavadinimas, kaina, stars, ivertinimas, prime, foto, link):
        self.pavadinimas = pavadinimas.strip()
        try:
            kainos_masyvas = []
            if len(kaina) > 7:
                for x in kaina.split("-"):
                    kainos_masyvas.append(float(x.strip("$ ")))
                self.kaina = kainos_masyvas
            else:
                kainos_masyvas.append(float(kaina.strip("$ ")))
                self.kaina = kainos_masyvas
        except ValueError:
            self.kaina = [00.01]
        ################################################################
        try:
            self.stars = int(stars)
        except ValueError:
            self.stars = 0
        #################################################################
        try:
            self.ivertinimas = float(ivertinimas[:3])
        except TypeError:  # kada kreivai pareina
            self.ivertinimas = 0
        except ValueError:  # kada prime ateina
            self.ivertinimas = 0
        # ###############################################################
        self.prime = prime
        self.foto = foto
        self.link = "https://www.amazon.com" + link
        preke.autoNr += 1
        self.id = preke.autoNr

    def viskas(self):
        return "ID:{}\nPv:{}\nKN:{}\nST:{}\nIV:{}\nPR:{}\nFT:{}\nLI:{}".format(self.id, self.pavadinimas, self.kaina,
                                                                               self.stars, self.ivertinimas, self.prime,
                                                                               self.foto, self.link)

    def irasyti_i_db_lentele(self, lentele, kategorija):
        if len(self.kaina) == 2:
            return """INSERT INTO `{}` (`pavadinimas` , `kategorija`,`kaina`, `ivertinimas`, `stars`, `prime`, `foto`, `link`) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')""".format(
                lentele, self.pavadinimas.translate({ord(c): None for c in "'`"}), kategorija, self.kaina[0],
                self.ivertinimas, self.stars, self.prime, self.foto,
                self.link) + """,('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');""".format(
                self.pavadinimas.translate({ord(c): None for c in "'`"}), kategorija, self.kaina[1], self.ivertinimas,
                self.stars, self.prime, self.foto, self.link)
        else:
            return """INSERT INTO `{}` (`pavadinimas`, `kategorija`, `kaina`, `ivertinimas`, `stars`, `prime`, `foto`, `link`) VALUES ('{}','{}', '{}', '{}', '{}', '{}', '{}', '{}');""".format(
                lentele, self.pavadinimas.translate({ord(c): None for c in "'`"}), kategorija, self.kaina[0],
                self.ivertinimas, self.stars, self.prime, self.foto, self.link)



# grazina url lista
def psl_scrap(url, proxies):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
    re = requests.get(url, headers=headers)  # , proxies=proxies)
    re.raise_for_status()
    # viskas eina per proxy serveri
    print("atsiuncia:\n{}".format(url))

    # cia siuncia viena psl
    objektuMasyvas = []

    soup = bs4.BeautifulSoup(re.text, "lxml")
    visi_elementai = soup.find_all("div", class_="zg_itemWrapper")

    for x in visi_elementai:
        # pavadinimas
        try:
            pavadinimas = x.find(class_="p13n-sc-truncate p13n-sc-line-clamp-2").get_text()
        except AttributeError:
            try:
                pavadinimas = x.find(class_="p13n-sc-truncate p13n-sc-line-clamp-3").get_text()
            except AttributeError:
                pavadinimas = "nera pavadinimo"
        # kaina
        try:
            kaina = x.find(class_="p13n-sc-price").get_text()
        except AttributeError:
            kaina = "nera kainos"
        # stars
        try:
            stars = x.find(class_="a-size-small a-link-normal").get_text()
        except AttributeError:
            stars = "nera stars"
        # ivertinimas
        try:
            # ivertinimas = x.find(class_="a-icon-alt").get_text()
            ivertinimas = x.find_all("span", class_="a-icon-alt")
        except AttributeError:
            ivertinimas = "nera ivertinimas"
        prime = 0
        if len(ivertinimas) == 2:
            for y in ivertinimas:
                try:
                    vert = str(y).split(">")[1].split("<")[0]
                except AttributeError:
                    vert = "nera"
                if vert == "Prime":
                    prime = 1
                else:
                    ivertinimas = vert
        else:
            for y in ivertinimas:
                try:
                    vert = str(y).split(">")[1].split("<")[0]
                except AttributeError:
                    vert = "nera"
                if vert == "Prime":
                    prime = 1
                else:
                    ivertinimas = vert
        # paveikslelis
        try:
            foto = x.findAll('img')[0].get('src')
        except:
            # kartais buna AttributeError
            # kartais out of range
            foto = 'nera paveikslelis'
        # link
        try:
            link = x.find("a", class_="a-link-normal").get('href')
        except AttributeError:
            link = "nera linko"
        objektuMasyvas.append(preke(pavadinimas, kaina, stars, ivertinimas, prime, foto, link))
    return objektuMasyvas
