import urllib.request
import urllib.parse
import re
import matplotlib.pyplot as plt
import sys


def get_actor_page(actor_name):
    # This section gets the actor's name
    actor_name = actor_name.strip()

    # This section gets the segment of the URL specific to the actor in question
    actor_url = actor_name.lower()
    while "." in actor_url:
        actor_url = actor_url.replace(".","")

    actor_url = actor_url.replace(" ", "_")

    actor_page = 'https://www.rottentomatoes.com/celebrity/' + actor_url

    return actor_page


def web_scrape(actor_page):
    try:
        resp = urllib.request.urlopen(actor_page)
    except Exception as e:
        return False
    else:
        resp_data = resp.read()

    # Add search for actor's namet
    name_search = re.search(r"""(?P<actor_name>[\w.:\- ]+)</h1>""",
                             str(resp_data), re.X)
    name = name_search.group('actor_name')

    start_point = re.search(r"""<h2>MOVIES</h2>\\n""", str(resp_data))
    if start_point is not None:
        start_point = start_point.end()
    else:
        return False

    end_point = re.search(r"""<h2>TV</h2>""", str(resp_data))
    if end_point is not None:
        end_point = end_point.start()

    score_search = re.findall(r"""<td\sdata-rating=\"(?P<score>[\d]+)\"\sdata-title=\"(?P<title>[\w: ]+)\"
                               [\w \\<>'/"=-]+<span[ ]class=\"tMeterScore">[\d]+%</span>
                               [\w\s \\'/"-=]+</span>[\w\s \\'/"-=]+</td>[\w\s \\'/"-=]+>
                               [\w\s \\'/"-=]+href="(?P<url>[/\w_]+)">[\w\s \\'/"-=:<\.]+>[\D]+>
                               #[\w\s \\'/"-=]+>[\w\s \\'/"-=]+>[\w\s \\'/"-=]+>[\w\s \\'/"-=]+>
                               [\w\s \\'/"-=]+>[\w\s \\'/"-=]+>#[\w\s \\'/"-=]+>#[\w\s \\'/"-=]+>
                               [\w\s \\'/"-=]+>(?P<year>\d{4})</td>
                               """, str(resp_data)[start_point:end_point], re.X)

    score_search = score_search[::-1] # reverse the search to be chronological order

    return name, score_search # soon to return actor's name as well


def graph_data(data):
    actor_name, score_data = data

    length = len(score_data)

    movie_number = [n+1 for n in range(length)]
    score_array = [movie[0] for movie in score_data]

    title_array = [movie[1] for movie in score_data]
    url_array = ["https://www.rottentomatoes.com" + movie[2] for movie in score_data]
    year_array = [movie[3] for movie in score_data]

    # fig = plt.figure()

    plt.scatter(movie_number, score_array)

    plt.title(actor_name, fontsize=24)
    plt.xlabel("Movie Number", fontsize=14)
    plt.ylabel("Tomatometer", fontsize=14)
    plt.tick_params(axis='both', which='major', labelsize=14)
    plt.subplots_adjust(left=0.16, bottom=0.12, right=0.94, top=0.90, wspace=0.2, hspace=0)
    plt.grid(b=True, which="major", axis="y")

    plt.show()


def main(actor_name):
    actor_page = get_actor_page(actor_name)
    score_data = web_scrape(actor_page)
    print(score_data)


if __name__ == "__main__":
    actor_name = input("Enter name: ")
    main(actor_name)