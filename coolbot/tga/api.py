import requests
import json

BASE_URL = "http://127.0.0.1:8000/api/"

def create_user(username, name, user_id):
    url = f"{BASE_URL}botuser/"
    response = requests.get(url=url).text
    data = json.loads(response)
    user_exist = False
    for i in data:
        if i['user_id']== str(user_id):
            user_exist =True
            break
    if user_exist == False:
        requests.post(url=url, data={"username":username, "name":name, "user_id":user_id})
        return "User yaratildi."
    else:
        return "User mavjud"


create_user("@Buy9663", "MuhammadAmin", "12312341241")

def create_feedback(user_id,body):
    url = f"{BASE_URL}feed/"
    if body and user_id:
        requests.post(url=url, data={
            "user_id":user_id,
            "body":body
        })
        return "Adminga yuborildi raxmat sz bilan bog'lanadi!!."
    else:
        return "Userni commenti oxiriga yetmadi"

print(create_feedback("12312434124", "zor emas"))


