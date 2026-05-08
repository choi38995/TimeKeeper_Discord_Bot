import os
import requests
import json
import base64

GIT_TOKEN = os.getenv("DATA_GIT_TOKEN")
GIT_URL = os.getenv("GIT_PATH_SCRIPTS")

headers = {
    "Authorization": f"token {GIT_TOKEN}",
    "Accept": "application/vnd.github+json"
}


# 최초 실행해 해당 파일 내용을 읽어와 메모리/캐시 에 담아두고 1시간 간격으로 수정
# 최초 실행 1번만 호출
# TODO: sha 캐싱하기
def load_user():
    # Get the file content
    response = requests.get(GIT_URL+"/user_info.json", headers=headers)
    # 성공 할 경우, 파일 내용이 base64로 인코딩되어 있으므로 디코딩
    # dict 형태로 반환
    if response.status_code == 200:
        content = response.json().get("content")
        decoded_content = base64.b64decode(content).decode("utf-8")
        # json.loads로 다시 json 형태로 변환
        get_json = json.loads(decoded_content)
        # dict 형태로 변환 및 반환
        return conversion_dict(get_json)
    else:
        # raise은 일부러 예외를 발생시키는 키워드입니다. 
        # 예외가 발생하면 프로그램이 중단되고, 예외 메시지가 출력됩니다.
        # try-except 블록에서 예외를 처리할 때,
        #  except 블록에서 raise를 사용하여 예외를 다시 발생시킬 수 있습니다.
        raise Exception(f"Failed to load user data: {response.status_code} - {response.text}")


# sha로 파일 업데이트하기
# TODO: 캐싱 된 sha 사용하기
# TODO: 스케줄을 돌려 1시간 마다 git에 업데이트하기
def update_user(data):
    sha = file_data["sha"]
    content = base64.b64encode(json.dumps(conversion_json(data)).encode("utf-8")).decode("utf-8")
    payload = {
        "message": "Update user data",
        "content": content,
        "sha": sha
    }
    response = requests.put(GIT_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        # raise은 일부러 예외를 발생시키는 키워드입니다. 
        # 예외가 발생하면 프로그램이 중단되고, 예외 메시지가 출력됩니다.
        # try-except 블록에서 예외를 처리할 때,
        #  except 블록에서 raise를 사용하여 예외를 다시 발생시킬 수 있습니다.
        raise Exception(f"Failed to update user data: {response.status_code} - {response.text}")
    

def conversion_dict(json_data: json):
    temp = json_data.get("user")
    # json_data는 dict 형태로 전달
    # dict 형태로 반환
    users: dict[str, dict[str, object | None]] = {}
    for value in temp.items():
        users[value.get("id")] = {
            "start_time": value.get("start_time"),
            "end_time": value.get("end_time"),
            "status": value.get("status"),
            "reason": value.get("reason")
        }

    return users

def conversion_json(users: dict[str, dict[str, object | None]]):
    # dict 형태로 전달
    # json 형태로 반환
    temp = []
    for key, value in users.items():
        temp.append({ 
            "id": key,
            "start_time": value.get("start_time"),
            "end_time": value.get("end_time"),
            "status": value.get("status"),
            "reason": value.get("reason")
        })
    return {"user": temp}
