import requests
import json

url = "https://poe.com/api/gql_POST"

payload = json.dumps({
   "queryName": "sendMessageMutation",
   "variables": {
      "chatId": 603681959,
      "bot": "capybara",
      "query": "你好你是十二？",
      "source": {
         "sourceType": "chat_input",
         "chatInputMetadata": {
            "useVoiceRecord": False
         }
      },
      "clientNonce": "7jlDbV5FDDqk177n",
      "sdid": "1a0d6554-e416-491a-94a1-ef044404921c",
      "attachments": [],
      "existingMessageAttachmentsIds": [],
      "shouldFetchChat": False,
      "messagePointsDisplayPrice": 20
   },
   "extensions": {
      "hash": "bfeedf7c108ea69eab4b432c85b28b4dc76c6376453002f6b45d47cc1b568daf"
   }
})
headers = {
   'Cookie': '__cf_bm=3hgga7LeEN9yOcC2hCEpVfOzqzBvxqI.Y_o1d3ZQsKg-1722667756-1.0.1.1-IQz76QQvbA7Po0diexnpK1GOgom9r4FHQ1e3aiS1hTKpEwuAOmAfvK6Z7hWUqRqVZ4bsddSVUz.kewtKDT099g; p-b=RLx7wyTl7EqmZF6AGj6Now%3D%3D; cf_clearance=LRcf5Zy1whhOYh3YoNLAoAyBsm6rppbujxVWOiglvz0-1722667757-1.0.1.1-yRRht8Zbbiilb.lgD0vh0YqbN3x4FvcIDKD_K4dwWaGe1udBOVguIvEGNPZUkeY6XXHc8DsUvZF1E3w7XzC8hw; _gcl_au=1.1.1957160826.1722667758; _fbp=fb.1.1722667759558.673906808507144637; p-lat=8j%2FB%2BZLECIOkOfMMgilmKpmCPEDccjPlhWCPh4KAkA%3D%3D; OptanonConsent=isGpcEnabled; OptanonAlertBoxClosed=2024-08-03T06:49:26.061Z',
   # 'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
   'Content-Type': 'application/json'
}
response = requests.request("POST", url, headers=headers, data=payload)


print(response.text)
