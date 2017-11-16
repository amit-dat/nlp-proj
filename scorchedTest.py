import scorched
si = scorched.SolrInterface('http://localhost:8983/solr/mycore2')

document = {"id": "0553573403",
            "cat": "book",
            "name": "A Game of Thrones",
            "price": 7.99,
            "inStock": True,
            "author_t": "George R.R. Martin",
            "series_t": "A Song of Ice and Fire",
            "sequence_i": 1,
            "genre_s": "fantasy"}

si.add(document)
si.commit()

response = si.query("*").execute()

print("Status: ", response.status)
print("QTime: ", response.QTime)
print("Params: ", response.params)
print("Result: ", response.result)
print("\n")

for result in response:
    for key, val in result.items():
        print("{}: {}".format(key, val))
