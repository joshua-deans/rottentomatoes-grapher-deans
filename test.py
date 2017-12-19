import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import re
import matplotlib.pyplot as plt
import random

actor_url = "christopher_nolan"

actor_page = 'https://www.rottentomatoes.com/celebrity/' + actor_url

try:
    resp = urllib.request.urlopen(actor_page)
except:
    print("Error found: Name given is invalid ")
else:
    data = resp.read()
    # data = resp.readlines()

#length = len(data)

#for i in range(length):
#    print(data[i])

# [\w?=&-\\/"' <>:#;]+


start_point = re.search(r"""<h2>MOVIES</h2>\\n""", str(data))
start_point = start_point.end()

end_point = re.search(r"""<h2>TV</h2>""", str(data))
end_point = end_point.start()


score_search = re.findall(r"""<td\sdata-rating=\"(?P<score>[\d]+)\"\sdata-title=\"(?P<title>[\w: ]+)\"
                           [\w \\<>'/"=-]+<span[ ]class=\"tMeterScore">[\d]+%</span>
                           [\w\s \\'/"-=]+</span>[\w\s \\'/"-=]+</td>[\w\s \\'/"-=]+>
                           [\w\s \\'/"-=]+href="(?P<url>[/\w_]+)">[\w\s \\'/"-=:<\.]+>[\D]+>
                           #[\w\s \\'/"-=]+>[\w\s \\'/"-=]+>[\w\s \\'/"-=]+>[\w\s \\'/"-=]+>
                           [\w\s \\'/"-=]+>[\w\s \\'/"-=]+>#[\w\s \\'/"-=]+>#[\w\s \\'/"-=]+>
                           [\w\s \\'/"-=]+>(?P<year>\d{4})</td>
                           """, str(data)[start_point:end_point], re.X)

'''
score_search = re.findall(r"""<td\sdata-rating=\"(?P<score>[\d]+)\"\sdata-title=\"(?P<title>[\w: ]+)\"
                               [\w \\<>'/"=-]+<span[ ]class=\"tMeterScore">[\d]+%</span>
                               [\w\s \\'/"-=]+</span>[\w\s \\'/"-=]+</td>[\w\s \\'/"-=]+>
                               [\w\s \\'/"-=]+href="(?P<url>[/\w_]+)">
                               """, str(resp_data)[start_point:end_point], re.X)
'''
#year_search = re.findall(r"""(?P<year>\d{4})</td>
#                           """, str(data)[start_point:end_point], re.X)

#print(year_search)

#length = len(score_search)

#for i in range(length):
#    score_search[i] += (str(year_search[i]),)

print(score_search)
