from dictionary import Dictionary
from client import Client

"""
Manages a dictionary of approved column descriptions from Alation
"""

# api token info: https://developer.alation.com/dev/docs/authentication-into-alation-apis
api_token = "<YOUR API TOKEN>"

dictionary = Dictionary()
client = Client(api_token)

for record in client.api_response():
    dictionary.add(record)

dictionary.save()
print(dictionary.fuzzy_lookup("something", threshold=90))
