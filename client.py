import time
import requests

resp = requests.post("http://127.0.0.1:5000/upscale",
                     files={"image": open("lama_300px.png", "rb")},
                     )

resp_data = resp.json()
print(resp_data)
task_id = resp_data.get("task_id")
print()




resp = requests.get(f"http://127.0.0.1:5000/tasks/<{task_id}>",
                    task_id
                    )
print(resp.json())
print('начало спанья')
time.sleep(3)
print('конец спанья')
resp = requests.get(f"http://127.0.0.1:5000/tasks/<{task_id}>",
                    task_id
                    )
print(resp.json())
# print('пока норм')
# print(resp.json())
# print(resp_data)
resp = requests.get(f"http://127.0.0.1:5000/processed/upscale_image.png",
                    task_id
                    )

