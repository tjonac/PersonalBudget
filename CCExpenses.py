import fitz
from bs4 import BeautifulSoup
import csv
class Expenses():
    def __init__(self, fileName: str, year: str):
        self.fileName = fileName
        self.year = year
        self.pdfFileName = rf"Data\pdfFiles\{fileName}.pdf"
        self.htmlFileName = rf"Data\htmlFiles\{fileName}.html"
        doc = fitz.open(self.pdfFileName)
        html = ''
        for num_pagina in range(2,len(doc)):
            pagina = doc.load_page(num_pagina)
            html += pagina.get_text("html")

        with open(self.htmlFileName, 'w', encoding="utf-8") as file:
            file.write(html)

        self.soup = BeautifulSoup(html, "lxml")
        self.headers = ["timestamp", "type", "description", "value"]
        self.data = []


    def to_num(x: str):
        return float(x.replace('$','').replace(',','').replace(' ',''))

    def is_date(x:str):
        temp = x.split(' ')
        months = set([
            "ENE", "FEB", "MAR", "ABR", "MAY", "JUN",
            "JUL", "AGO", "SEP", "OCT", "NOV", "DIC"
        ])
        try:
            int(x[0])
        except:
            return False
        if(len(temp) != 2): return False

        return (temp[1] in months)

    def to_date(self, x:str):
        temp = x.split(' ')
        months = {
            "ENE": "01",
            "FEB": "02",
            "MAR": "03",
            "ABR": "04",
            "MAY": "05",
            "JUN": "06",
            "JUL": "07",
            "AGO": "08",
            "SEP": "09",
            "OCT": "10",
            "NOV": "11",
            "DIC": "12"
        }
        temp[1]=months[temp[1]]
        temp.append(self.year)

        return temp[0]+'-'+temp[1]+'-'+temp[2]

    def nu(self):
        tags = self.soup.find_all("span")
        i = 0
        while i < len(tags):
            tag = tags[i].text.strip()
            while(not Expenses.is_date(tag) and tag != "Saldo final del periodo"):
                i+=1
                tag = tags[i].text.strip()
            if(tag == "Saldo final del periodo"): break
            else:
                temp = []
                for j in range(4):
                    if(j == 0): temp.append(Expenses.to_date(self,tag))
                    elif(j == 3): temp.append(Expenses.to_num(tag))
                    else: temp.append(tag)
                    i+=1
                    tag = tags[i].text.strip()
                self.data.append(temp)


        with open(rf"Data\parsed\{self.fileName}.csv", 'w', newline='', encoding="utf-8") as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(self.headers)
            writer.writerows(self.data)

