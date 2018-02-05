from google import google

num_page = 5

query = "https://www.infobae.com/politica/2017/09/18/"

response = google.search(query, num_page, lang = 'es')

aux_func = lambda x: query in x.link

good_results = filter(aux_func, response)

for result in good_results:
    print result.link


