import re

with open('BestBooksEver.html') as f:
    vsebina = f.read()

vzorec = (
    r'data-resource-type="Book">\n.*<a title='
    r'"(?P<naslov>.*?)"' #zajamem naslove
    r'.*(\n.*){11}itemprop="name">'
    r'(?P<avtor>.*?)<' #zajamem avtorje
)

for zadetek in re.finditer(vzorec, vsebina):
    print (zadetek.groupdict())

