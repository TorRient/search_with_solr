import pysolr
import json
from solrq import Q
from pyvi import ViTokenizer
# Setup a Solr instance. The timeout is optional.
solr = pysolr.Solr('http://localhost:8983/solr/bkcv', always_commit=True, timeout=100)

# # general_text = ''
title = ViTokenizer.tokenize("Ba ôtô dàn hàng ngang vượt đèn đỏ")
# print(title)
# query = Q(title="\"{}\"".format(title))^2 \
#         | Q(description="Hải Phòng Khi tín hiệu đèn đỏ còn ở giây")^1

query = Q(content="\"Nước Anh chính_thức phong_tỏa\"")
print(query)
results = solr.search(str(query).replace("\\",""), **{
        'rows':100000,
        'hl':'true',
        'hl.method':'original',
        'hl.simple.pre':'<mark style="background-color:#ffff0070;">',
        'hl.simple.post':'</mark>',
        'hl.highlightMultiTerm':'true',
        'hl.fragsize':100,
        'defType' : 'edismax',
        'fl' : '*, score',
        # 'bq':'{!func}linear(clicked, 0.01 ,0.0 )',
        # # 'bq':'{!func}log(linear(clicked, 20 ,0.0 ))',
        'mm':1,
        'ps':3,
        'pf': 'topic^1 title^1 content^1 author^1 description^1 publish_date^1',
        'qf': 'topic^1 title^1 content^1 author^1 description^1 publish_date^1',
    })

# results = solr.search('Ánh_Dương', **{
#         'rows':100000,
#         'hl':'true',
#         'hl.method':'original',
#         'hl.simple.pre':'<mark style="background-color:#ffff0070;">',
#         'hl.simple.post':'</mark>',
#         'hl.highlightMultiTerm':'true',
#         'hl.fragsize':100,
#         'defType' : 'dismax',
#         'fl' : '*, score',
#         # 'bq':'{!func}linear(clicked, 0.01 ,0.0 )',
#         # # 'bq':'{!func}log(linear(clicked, 20 ,0.0 ))',
#         'mm':1,
#         'ps':3,
#         # 'pf': 'title description',
#         'qf': 'title description author',
#     })
# print(dir(results.highlighting.get))
print(results.highlighting.values())
print(len(results))
# print("tet:", results)
for idx, i in enumerate(results):
    print('he')
    print(i["content"])
    # print(i["description"])
    # if idx == 0:
    #     break
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