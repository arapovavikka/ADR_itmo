#get topics from private group

import requests
import json
import time
#создаем csv
import csv
from collections import namedtuple
#для даты и времени
from datetime import date

domain = "psy_pharmacy"

# специальный id группы в вк
owner_id = "179715168"

# стандартные данные для запроса 
# тут твой токен, который запрашивается вот так https://vk.com/dev/auth_sites
access_token ="fc9348e92d6d2bf89bdbe5b0ff1ced793433aacd9e9919d6bce3f90bb5195ba3915104381900ee7e548e9"
v = "5.103"

result_filename = "boards_topics_ids_" + str(date.today()) + ".csv"

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

def getCommentsFromTopic(topic_id):
	resp = requests.get('https://api.vk.com/method/board.getComments?group_id={0}&topic_id={1}&v={2}&access_token={3}'.format(owner_id, topic_id, v, access_token))

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

rows = []
with open(result_filename, 'w', newline='', encoding='utf-16') as csvFile:
	fieldnames=['topic_id','id','text']
	writer = csv.DictWriter(csvFile, fieldnames)
	rows.append({'topic_id':'Topic Id', 'id': "Id",'text': "Text"})
	for item in resp_content:
		rows.append({'topic_id': item['id'],'id': "-",'text': item['title']})

		#иногда по таймауту возвращается ошибка из-за того что слишком много запросов в секунду
		time.sleep( 0.5 )

		content_comments, topics_total_comments = getCommentsFromTopic(item['id'])
		for comment_item in content_comments:
			#иногда по таймауту возвращается ошибка из-за того что слишком много запросов в секунду
			time.sleep( 0.5 )
			rows.append({'topic_id': item['id'],'id': comment_item['id'],'text': comment_item['text']})
	writer.writerows(rows)

