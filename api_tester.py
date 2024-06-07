import requests

# Define the GraphQL query
query = '''
    query {
      user(age: 31) {
        id
        name
        age
      }
    }
'''

response = requests.post('http://localhost:8000/graphql', json={'query': query})

if response.status_code == 200:
    data = response.json()

    print(data)
else:
    print("Error:", response.text)
