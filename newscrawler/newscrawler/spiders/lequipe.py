import scrapy
import csv
from scrapy import Request


class LemondeSpider(scrapy.Spider):
    name = "lequipe"
    allowed_domains = ["www.lequipe.fr"]
    start_urls = ['https://www.lequipe.fr']
    joueurs = []
    années = []

    def parse(self, response):
        #title = response.css('title::text').extract_first()
        
        yield Request("https://www.lequipe.fr/Tennis/atp/epreuve-simple-messieurs/page-palmares-individuel/par-annee",callback=self.parse2)
        yield Request("https://www.lequipe.fr/Tennis/roland-garros/epreuve-simple-messieurs/page-palmares-individuel/par-annee",callback=self.parse3,meta={'name': 'rolland garros men'})
        yield Request("https://www.lequipe.fr/Tennis/us-open/epreuve-simple-messieurs/page-palmares-individuel/par-annee",callback=self.parse3,meta={'name': 'us open men'})
        yield Request("https://www.lequipe.fr/Tennis/open-d-australie/epreuve-simple-messieurs/page-palmares-individuel/par-annee",callback=self.parse3,meta={'name': 'open australie men'})
        yield Request("https://www.lequipe.fr/Tennis/wimbledon/epreuve-simple-messieurs/page-palmares-individuel/par-annee",callback=self.parse3,meta={'name': 'wimbledon men'})
        yield Request("https://www.lequipe.fr/Tennis/wta/epreuve-simple-dames/page-palmares-individuel/par-annee",callback=self.parse2)
        yield Request("https://www.lequipe.fr/Tennis/roland-garros/epreuve-simple-dames/page-palmares-individuel/par-annee",callback=self.parse3,meta={'name': 'rolland garros women'})
        yield Request("https://www.lequipe.fr/Tennis/us-open/epreuve-simple-dames/page-palmares-individuel/par-annee",callback=self.parse3,meta={'name': 'us open women'})
        yield Request("https://www.lequipe.fr/Tennis/open-d-australie/epreuve-simple-dames/page-palmares-individuel/par-annee",callback=self.parse3,meta={'name': 'open australie women'})
        yield Request("https://www.lequipe.fr/Tennis/wimbledon/epreuve-simple-dames/page-palmares-individuel/par-annee",callback=self.parse3,meta={'name': 'wimbledon women'})
    

    def parse2(self,response):
        joueur = response.css("a.Link.Palmares__victoryName::text").extract()
        joueurs = []
        for j in joueur:
            j = self.clean_spaces(j)
            if(j[len(j)-1] == ","):
                j = j[0:len(j)-2]
            joueurs.append(j)
        
        sous_listes = [joueurs[i:i + 3] for i in range(0, len(joueurs), 3)]
        années = []
        année = response.css("div.Link.router-link-exact-active.router-link-active::text").extract()
        for i in année:
            i = self.clean_spaces(i)
            années.append(i)
            
        if len(sous_listes) == len(années):
            for sous_liste, element in zip(sous_listes, années):
                sous_liste.insert(0, element)
        yield{
            "années":années,
            "joueurs":sous_listes
        }
 
        #with open('exemple.csv', 'w', newline='', encoding='utf-8') as fichier:
        #    writer = csv.writer(fichier)
        #    for ligne in sous_listes:
        #        writer.writerow(ligne)
    
    
    def parse3(self,response):
        
        name = response.meta.get('name', 'default_name')

        joueur = response.css("div.Palmares__victoryName::text").extract()
        looser = response.css("div.Palmares__looser > span::text").extract()
        score = response.css("div.Palmares__looser::text").extract()
        joueurs =[]
        loosers = []
        scores =[]
        for j in joueur:
            j = self.clean_spaces(j)
            if(len(j) != 0):
                joueurs.append(j)
        
        for l in looser:
            l = self.clean_spaces(l)
            if(len(l) != 0):
                loosers.append(l)
        
        for m in score:
            m = self.clean_spaces(m)
            if(m != "contre" and len(m) != 0):
                scores.append(m)
        
        année = response.css("a.Link::text").extract()
        années = []
        for i in année:
            i = self.clean_spaces(i)
            if(len(i)==4 and (i[0] == "1" or i[0] == "2")):
                années.append(i)
        
        yield{
            #"années":années,
            #"joueurs":joueurs,
            #"loosers":loosers
            "scores":scores
        }
        
        sous_listes = []
        for k in range(len(années)):
            sous_listes.append([années[k],joueurs[k],loosers[k],scores[k]])
        
        
        with open(name+'.csv', 'w', newline='', encoding='utf-8') as fichier:
            writer = csv.writer(fichier)
            writer.writerow(["Year","winner "+name,"finalist "+name,"Score Final"])
            for ligne in sous_listes:
                writer.writerow(ligne)
    
    def clean_spaces(self, string):
        if string:
            return " ".join(string.split())