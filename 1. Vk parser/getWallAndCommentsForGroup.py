import requests
import json
import time
#создаем csv
import csv
from collections import namedtuple

domain = "psy_pharmacy"

# специальный id группы в вк
owner_id = "-179715168"

# стандартные данные для запроса 
# тут твой токен, который запрашивается вот так https://vk.com/dev/auth_sites
access_token ="vk_token"
v = "5.102"

total_posts = 0
max_count = 100

def getWallContent(offset):
	resp = requests.get('https://api.vk.com/method/wall.get?owner_id={0}&domain={1}&offset={2}&count={3}&v={4}&access_token={5}'.format(owner_id, domain, offset, max_count, v, access_token))

	if resp.status_code != 200:
	    # This means something went wrong.
	    raise ApiError('GET /tasks/ {}'.format(resp.status_code))
	result = resp.json()


	data_first = json.dumps(result)
	data = json.loads(data_first)
	content = data["response"]
	total_posts = content["count"]
	content = content["items"]
	return content, total_posts


current_number = 0
resp_content, total_posts = getWallContent(current_number)
current_number = current_number + max_count
while current_number < total_posts:
	resp, total_posts = getWallContent(current_number)
	resp_content.extend(resp)
	current_number = current_number + max_count


def getCommentContent(post_id, offset):
	resp_com = requests.get('https://api.vk.com/method/wall.getComments?owner_id={0}&post_id={1}&count={2}&v={3}&access_token={4}'.format(owner_id, post_id, max_count, v, access_token))
	if resp_com.status_code != 200:
	    # This means something went wrong.
	    raise ApiError('GET /tasks/ {}'.format(resp_com.status_code))
	result = resp_com.json()
	print(result)

	data_first = json.dumps(result)
	data = json.loads(data_first)
	content = data["response"]
	content = content["items"]
	return content



rows = []
with open('wall_psy_with_comments.csv', 'w', newline='', encoding='utf-16') as csvfile:
	fieldnames=['parent_id','id','from_id','text']
	writer = csv.DictWriter(csvfile, fieldnames)
	rows.append({'parent_id': "Parent Id",'id': "Id",'from_id': "User or group id",'text': "Text"})
	for item in resp_content:
		current_number = current_number + 1;
		print("Текст поста: " + item["text"])
		print(item)
		rows.append({'parent_id': "0",'id': item['id'],'from_id': "-",'text': item['text']})
		resp_comments = getCommentContent(item['id'], 0)

		#иногда по таймауту возвращается ошибка из-за того что слишком много запросов в секунду
		time.sleep( 0.5 )

		for comment in resp_comments:
			id = -1
			if 'id' in comment:
				id = comment['id']
			from_id = -1
			if 'from_id' in comment:
				from_id = comment['from_id']
			text = "no text"
			if 'text' in comment:
				text = comment['text']
			#добавляем столбцы с данными в нужном порядке	
			rows.append({'parent_id': item['id'],'id': id,'from_id': from_id,'text': text})
	writer.writerows(rows)
	print('Прочитано {0} из {1}'.format(current_number, total_posts))

print("File wall_psy_with_comments.csv was generated in local path")
