import bs4
import json
import unidecode
from progressbar import ProgressBar
import urllib.request
class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"

opener = AppURLopener()
response = opener.open('http://httpbin.org/user-agent')
from urllib.request import urlopen as uReq
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup

# progressbar object
pbar = ProgressBar()

# write to json function
def writeToJSONFile(path, fileName, data):
    filePathNameWExt = './' + path + '/' + fileName + '.json'
    with open(filePathNameWExt, 'w') as fp:
        json.dump(data, fp)
# replace all those if statements with this clean function sOON
def objectExists(x):
	if (x != None):
		return x.span.text
	else:
		return ''

# path and name of file 
path = './'
fileName = 'zipcode-data-austin'
data = {}
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.8',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}

austin_urls = []
nyc_urls=[]
austin_zip_codes=map(str,[78610, 78613, 78617, 78641, 78652, 78653, 78660, 78664, 78681, 78701, 78702, 78703, 78704, 78705, 78712, 78717, 78719, 78721, 78722, 78723, 78724, 78725, 78726, 78727, 78728, 78729, 78730, 78731, 78732, 78733, 78734, 78735, 78736, 78737, 78738, 78739, 78741, 78742, 78744, 78745, 78746, 78747, 78748, 78749, 78750, 78751, 78752, 78753, 78754, 78756, 78757, 78758, 78759])
nyc_zip_codes=map(str,[10001, 10002, 10003, 10004, 10005, 10006, 10007, 10009, 10010, 10011, 10012, 10013, 10014, 10016, 10017, 10018, 10019, 10020, 10021, 10022, 10023, 10024, 10025, 10026, 10027, 10028, 10029, 10030, 10031, 10032, 10033, 10034, 10035, 10036, 10037, 10038, 10039, 10040, 10044, 10065, 10069, 10075, 10103, 10110, 10111, 10112, 10115, 10119, 10128, 10152, 10153, 10154, 10162, 10165, 10167, 10168, 10169, 10170, 10171, 10172, 10173, 10174, 10177, 10199, 10271, 10278, 10279, 10280, 10282, 10301, 10302, 10303, 10304, 10305, 10306, 10307, 10308, 10309, 10310, 10311, 10312, 10314, 10451, 10452, 10453, 10454, 10455, 10456, 10457, 10458, 10459, 10460, 10461, 10462, 10463, 10464, 10465, 10466, 10467, 10468, 10469, 10470, 10471, 10472, 10473, 10474, 10475, 11004, 11005, 11101, 11102, 11103, 11104, 11105, 11106, 11109, 11201, 11203, 11204, 11205, 11206, 11207, 11208, 11209, 11210, 11211, 11212, 11213, 11214, 11215, 11216, 11217, 11218, 11219, 11220, 11221, 11222, 11223, 11224, 11225, 11226, 11228, 11229, 11230, 11231, 11232, 11233, 11234, 11235, 11236, 11237, 11238, 11239, 11351, 11354, 11355, 11356, 11357, 11358, 11359, 11360, 11361, 11362, 11363, 11364, 11365, 11366, 11367, 11368, 11369, 11370, 11371, 11372, 11373, 11374, 11375, 11377, 11378, 11379, 11385, 11411, 11412, 11413, 11414, 11415, 11416, 11417, 11418, 11419, 11420, 11421, 11422, 11423, 11424, 11425, 11426, 11427, 11428, 11429, 11430, 11432, 11433, 11434, 11435, 11436, 11451, 11691, 11692, 11693, 11694, 11697])
for x in austin_zip_codes:
	austin_urls.append('https://www.niche.com/places-to-live/z/'+x+'/')
for y in nyc_zip_codes:
	nyc_urls.append('https://www.niche.com/places-to-live/z/'+y+'/')
#print(austin_urls)

print(len(austin_urls))
print(len(nyc_urls))
counter = 1
for url in pbar(austin_urls):
	print(counter)
	counter += 1
	my_url = url
	print(my_url)


	# opening connection, grabbing page
	req = Request(my_url, headers=HEADERS)
	webpage = urlopen(req, timeout=20).read()
	uClient = uReq(req)


	#offloads content to a variable
	page_html = uClient.read()

	# closes connection
	uClient.close()

	# html parsing
	page_soup = soup(page_html, "html.parser",from_encoding="iso-8859-1")

	# name of zipcode
	zipcode_name = page_soup.h1.text
	data[zipcode_name] = {}



	# 'niche report card' or 'niche grade'
	report_card = page_soup.find("div", {"class":"report-card"})
	grades = report_card.findAll("li", {"class":"ordered__list__bucket__item"})
	# dictionary in dictionary for niche report card
	data[zipcode_name]["niche_report_card"] = {}
	for grade in grades:
		grade_label = grade.div.select('div')[0].text
		grade_val = grade.div.select('div')[1].text
		data[zipcode_name]["niche_report_card"][grade_label] = grade_val
		#print(data[zipcode_name]["niche_report_card"][grade_label])

	writeToJSONFile(path, fileName, data)

fileName = 'zipcode-data-nyc'
counter = 1
for url in pbar(nyc_urls):
	print(counter)
	counter += 1
	my_url = url
	print(my_url)


	# opening connection, grabbing page
	req = Request(my_url, headers=HEADERS)
	webpage = urlopen(req, timeout=20).read()
	uClient = uReq(req)


	#offloads content to a variable
	page_html = uClient.read()

	# closes connection
	uClient.close()

	# html parsing
	page_soup = soup(page_html, "html.parser",from_encoding="iso-8859-1")

	# name of zipcode
	zipcode_name = page_soup.h1.text
	data[zipcode_name] = {}



	# 'niche report card' or 'niche grade'
	report_card = page_soup.find("div", {"class":"report-card"})
	grades = report_card.findAll("li", {"class":"ordered__list__bucket__item"})
	# dictionary in dictionary for niche report card
	data[zipcode_name]["niche_report_card"] = {}
	for grade in grades:
		grade_label = grade.div.select('div')[0].text
		grade_val = grade.div.select('div')[1].text
		data[zipcode_name]["niche_report_card"][grade_label] = grade_val
		#print(data[zipcode_name]["niche_report_card"][grade_label])

	writeToJSONFile(path, fileName, data)