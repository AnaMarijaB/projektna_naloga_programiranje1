import bs4

with open('BestBooksEver.html') as f:
    vsebina = f.read()

zupa = bs4.BeautifulSoup(vsebina, 'html.parser')

for znacka in zupa.find_all(attrs={"data-resource-type":"Book"}):
        znacka_z_naslovom = znacka.find_next_sibling('dev')
        print(znacka)
'''
vzorec = (
    r'data-resource-type="Book">\n.*<a title='
    r'"(?P<naslov>.*?)"' #zajamem naslove
    r'.*(\n.*){11}itemprop="name">'
    r'(?P<avtor>.*?)<' #zajamem avtorje
)

for zadetek in re.finditer(vzorec, vsebina):
    print (zadetek.groupdict())
'''