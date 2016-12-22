from urllib.request import urlopen
from bs4 import BeautifulSoup

# Should do data cleanup in this file
# Change "—" to '-'

html = urlopen("http://wiki.teamliquid.net/dota2/Players_(all)")

line_list = str(html.read()).split("\\n")

doc_str = ""
for line in line_list:
	if "<td> <a href=\"/dota2/" in line and not "Category" in line and not "class=\"new\"" in line:
		doc_str += line + "\n"

soup = BeautifulSoup(doc_str, 'html.parser')

for suffix in soup.find_all('a'):
	player_name = suffix['href'].split("/")[-1]

	dest = "http://wiki.teamliquid.net/dota2/index.php?title={}&action=edit&section=0".format(player_name)

	player_html = urlopen(dest)
	parsed = BeautifulSoup(player_html.read(), 'html.parser')
	info_block = parsed.find_all(id='wpTextbox1')

	player_file = open("data/" + player_name + ".txt", 'w')
	player_file.write(str(info_block))
	player_file.close()
	print(player_name + " download complete")

