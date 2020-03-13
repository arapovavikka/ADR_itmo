#get topics from private group

import requests
import json
import time
#создаем csv
import csv
from collections import namedtuple

domain = "psy_pharmacy"

# специальный id группы в вк
owner_id = "179715168"

# стандартные данные для запроса 
# тут твой токен, который запрашивается вот так https://vk.com/dev/auth_sites
access_token ="3a49d84fc863f9d56b17762c9e36073ebbab6fc3db745dfa3803f87d05841623515cefbbd1bc8b6176ffb"
v = "5.103"

total_posts = 0
max_count = 100

def getBoardTopicsIds(offset):
	resp = requests.get('https://api.vk.com/method/board.getTopics?group_id={0}&v={1}&access_token={2}'.format(owner_id, v, access_token))

	print("Resp.status_code: " + str(resp.status_code))
	if resp.status_code != 200:
	    # This means something went wrong.
	    raise ApiError('GET /tasks/ {}'.format(resp.status_code))
	result = resp.json()
	print(result)


	data_first = json.dumps(result)
	data = json.loads(data_first)
	content = data["response"]
	total_posts = content["count"]
	content = content["items"]
	return content, total_posts


current_number = 0
resp_content, total_posts = getBoardTopicsIds(current_number)
current_number = current_number + max_count