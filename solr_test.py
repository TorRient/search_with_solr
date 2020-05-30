import pysolr
import json
# Setup a Solr instance. The timeout is optional.
solr = pysolr.Solr('http://localhost:8983/solr/bkcv', always_commit=True, timeout=100)


general_text = "title:\"Ba ôtô dàn hàng ngang vượt đèn đỏ\""
results = solr.search(general_text, **{
        'rows':100000,
        'hl':'true',
        'hl.method':'original',
        'hl.simple.pre':'<mark style="background-color:#ffff0070;">',
        'hl.simple.post':'</mark>',
        'hl.highlightMultiTerm':'true',
        'hl.fragsize':100,
        'defType' : 'lucene',
        'fl' : '*, score',
        # 'bq':'{!func}linear(clicked, 0.01 ,0.0 )',
        # # 'bq':'{!func}log(linear(clicked, 20 ,0.0 ))',
        'mm':1,
        'ps':3,
        'pf': 'title description content',
        'qf': 'title description',
    })
# print(dir(results.highlighting.get))
# print(results.highlighting.values())
print(len(results))
# print("tet:", results)
for i in results:
    print('he')
    print(i["title"])
# solr.delete(q='*:*')
# # with open('quote.json') as json_file:
# #     data = json.load(json_file)

# # field = []
# # for idx, j in enumerate(data):
# #     if len(data[idx]["tags"]) == 0:
# #         field.append({"text": data[idx]["text"][0] + " " + data[idx]["author"][0] + " " + " "})
# #     else:
# #         text = data[idx]["text"][0] + " " + data[idx]["author"][0] + " "
# #         for tag in data[idx]["tags"]:
# #             text = text + tag + " "
# #         field.append({"text": text})
# # solr.add(field)

# # with open('author.json') as json_file:
# #     data = json.load(json_file)

# # field = []
# # for idx, j in enumerate(data):
# #     text = data[idx]["name"] + " "
# #     for born in data[idx]["born"]:
# #         text += born + " "
# #     text += data[idx]["description"]
# #     field.append({"text": text})

# # # How you'd index data.
# # solr.add(field)