import os
import requests
import json
import base64
import exception as ex

GIT_TOKEN: str | None = None
GIT_URL: str | None = None
sha : str = "" # 파일 업데이트 시 필요한 sha 값, 최초 실행 시 load_user 함수에서 초기화

headers: dict[str, str] = {}

def set_api_info():
    global GIT_TOKEN, GIT_URL, headers
    GIT_TOKEN = os.getenv("DATA_GIT_TOKEN")
    GIT_URL = os.getenv("GIT_PATH_SCRIPTS")
    headers = {
         "Authorization": f"token {GIT_TOKEN}",
         "Accept": "application/vnd.github+json"
    }


# 최초 실행해 해당 파일 내용을 읽어와 메모리/캐시 에 담아두고 1시간 간격으로 수정
# 최초 실행 시 또는 update 시킨 후에 호출
# TODO: sha 캐싱하기
def load_user():
    set_api_info()
    if not GIT_TOKEN:
        raise ex.emptyUserException("Git token is not set. Please set the GIT_TOKEN environment variable.")
    if not GIT_URL:
        raise ex.emptyUserException("Git URL is not set. Please set the GIT_PATH_SCRIPTS environment variable.")
    global sha
    # Get the file content
    url = GIT_URL+"/user_info.json"
    response = requests.get(url, headers=headers, timeout=10)
    # 성공 할 경우, 파일 내용이 base64로 인코딩되어 있으므로 디코딩
    # dict 형태로 반환
    if response.status_code == 200:
        data = response.json()
        sha = data['sha']
        content = data.get("content")
        if not content:
            raise ex.NullDataException("Content is null. The file may be empty or not properly formatted.")
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
        raise ex.emptyUserException(f"Failed to load user data: {response.status_code} - {response.text}")


# sha로 파일 업데이트하기
# TODO: 캐싱 된 sha 사용하기
# TODO: 스케줄을 돌려 1시간 마다 git에 업데이트하기
def update_user(data):
    set_api_info()
    if not GIT_TOKEN:
        raise ex.emptyUserException("Git token is not set. Please set the GIT_TOKEN environment variable.")
    if not GIT_URL:
        raise ex.emptyUserException("Git URL is not set. Please set the GIT_PATH_SCRIPTS environment variable.")
    global sha

    content = None

    if data is None:
        temp = {"user": []}
        content = base64.b64encode(json.dumps(temp).encode("utf-8")).decode("utf-8")
    else :
        content = base64.b64encode(json.dumps(conversion_json(data)).encode("utf-8")).decode("utf-8")
  
    payload = {
        "message": "Update user data",
        "content": content,
        "sha": sha
    }
    url = GIT_URL+"/user_info.json"
    response = requests.put(url, headers=headers, json=payload, timeout=10)
    if response.status_code == 200 or response.status_code == 201:
        data = response.json()        
        sha = data['content']['sha']
        return base64.b64decode(data["content"]).decode("utf-8")
    else:
        # raise은 일부러 예외를 발생시키는 키워드입니다. 
        # 예외가 발생하면 프로그램이 중단되고, 예외 메시지가 출력됩니다.
        # try-except 블록에서 예외를 처리할 때,
        #  except 블록에서 raise를 사용하여 예외를 다시 발생시킬 수 있습니다.
        raise ex.emptyUserException(f"Failed to update user data: {response.status_code} - {response.text}")
    

def conversion_dict(json_data: dict[str, object]):
    temp = json_data.get("user", [])
    # json_data는 dict 형태로 전달
    # dict 형태로 반환
    users: dict[str, dict[str, object | None]] = {}
    for value in temp:
        if not value.get("id"):
            raise ex.NullDataException("User ID is null. Each user entry must have a valid ID.")    
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
