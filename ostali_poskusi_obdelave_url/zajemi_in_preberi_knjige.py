import json
import re
import requests
import orodja

with open('BestBooksEver.html') as f:
    vsebina = f.read()

vzorec_bloka = re.compile(
    r'data-resource-type="Book".*?'
    r'alt="Loading trans"',
    flags=re.DOTALL
)

for zadetek in re.finditer(vzorec_bloka, vsebina):
    print (zadetek.groupdict())

vzorec = (
    r'data-resource-type="Book">\n.*<a title='
    r'"(?P<naslov>.*?)"' #zajamem naslove
    r'.*(\n.*){11}itemprop="name">'
    r'(?P<avtor>.*?)<' #zajamem avtorje
)

stevilo_vseh_strani = 6
count=0
knjige = []

for st_strani in range(1,stevilo_vseh_strani,1):
    url = (
        'https://www.goodreads.com/list/show/'
        '1.Best_Books_Ever?'
        f'page={st_strani}'
    )
    ime_datoteke = f'knjige-{st_strani}.html'
    orodja.shrani_spletno_stran(url, ime_datoteke)
    vsebina = orodja.vsebina_datoteke(ime_datoteke)
    for zadetek in re.finditer(vzorec,vsebina):
        knjige.append(zadetek.groupdict())
        count += 1





orodja.zapisi_json(knjige, 'knjige.json')


