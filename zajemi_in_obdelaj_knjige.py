
import json
import re
import requests
import orodja

vzorec_bloka = re.compile(
    r'<tr itemscope itemtype="http://schema.org/Book".*?'
    r'</div>\s*</td>\s*</tr>',
    flags=re.DOTALL
)

vzorec_knjige = re.compile(
    r'data-resource-type="Book">\n.*<a title='
    r'"(?P<naslov>.+?)".*?' #zajamem naslove
    r'itemprop="name">'
    r'(?P<avtor>.*?)<' , #zajamem avtorje
    flags=re.DOTALL
)

vzorec_rating = re.compile(
    r'<span class="minirating">.*?</span></span>'
    r'(?P<rating>.*?)'
    r'avg rating &mdash; '
    r'(?P<vsi_ratings>.*?) ratings',
    flags=re.DOTALL
)

vzorec_score = re.compile(
    r'<span class="smallText uitext">.*?'
    r'score: (?P<score>.*?)</a>.*?'
    r'return false;">(?P<people_voted>.*?) people voted',
    flags=re.DOTALL
)


def izloci_podatke_knjige(blok):
    knjiga = vzorec_knjige.search(blok).groupdict()
    knjiga['naslov']= knjiga['naslov']
    knjiga['avtor'] = knjiga['avtor']

    povp_ocena = vzorec_rating.search(blok)
    knjiga['ocena'] = povp_ocena['rating']
    knjiga['vse_ocene'] = povp_ocena['vsi_ratings']

    koncna_ocena =vzorec_score.search(blok)
    if koncna_ocena:
         knjiga['kon_ocena'] = koncna_ocena['score'].replace(',','.')
    else:
        knjiga['kon_ocena']=None

    knjiga['vsi_glasovi'] = int(float(koncna_ocena['people_voted'].replace(',','')))

    return knjiga

def knjige_na_strani(st_strani, na_stran = 100):
    url = (
        'https://www.goodreads.com/list/show/'
        '1.Best_Books_Ever?'
        f'page={st_strani}'
    )
    ime_datoteke = f'htmlji/knjige-{st_strani}.html'
    orodja.shrani_spletno_stran(url, ime_datoteke)
    vsebina = orodja.vsebina_datoteke(ime_datoteke)
    for blok in vzorec_bloka.finditer(vsebina):
        yield izloci_podatke_knjige(blok.group(0))


knjige = []
for st_strani in range(1,7):
    for knjiga in knjige_na_strani(st_strani, 100):
        knjige.append(knjiga)

knjige.sort(key=lambda ocena: knjiga['ocena'])
orodja.zapisi_json(knjige, 'obdelani-podatki/knjige.json')

orodja.zapisi_csv(
    knjige,
    ['naslov', 'avtor', 'ocena', 'vse_ocene', 'kon_ocena', 'vsi_glasovi'], 'obdelani-podatki/knjige.csv'
)

def izloci_gnezdene_podatke(knjige):
    ocene, avtorji, popularnost = [], [], []
    
    for knjiga in knjige:
            ocene.append({'naslov':knjiga['naslov'], 'ocena':knjiga['ocena'] })
            avtorji.append({'avtor':knjiga['avtor'], 'odlocilna_ocena':knjiga['kon_ocena']})
            popularnost.append({'naslov':knjiga['naslov'], 
                                'odlocilna_ocena':knjiga['kon_ocena'], 
                                'vsi_glasovi':knjiga['vsi_glasovi']})
        
    ocene.sort(key=lambda naslov: naslov['ocena'])
    popularnost.sort(key=lambda naslov: naslov['vsi_glasovi'])

    return ocene, avtorji, popularnost

ocene, avtorji, popularnost = izloci_gnezdene_podatke(knjige)
orodja.zapisi_csv(ocene, ['naslov', 'ocena'], 'obdelani-podatki/ocena.csv')
orodja.zapisi_csv(avtorji, ['avtor', 'odlocilna_ocena'], 'obdelani-podatki/avtorji.csv')
orodja.zapisi_csv(popularnost, ['naslov', 'odlocilna_ocena','vsi_glasovi'], 'obdelani-podatki/popularnost.csv')