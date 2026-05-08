import status
# TODO : 깃헙 private repository에서 데이터 관리를 위한 코드 작성
# 딕셔너리 생성이란? 기본 데이터 구조를 넣는 것을 의미합니다. 
# 딕셔너리는 키-값 쌍으로 데이터를 저장하는 자료구조입니다.
# java로 친다면 List<Map<String, Object>> users = new ArrayList<>();
users: dict[str, dict[str, object | None]] = {}

# 일별로 봇 실행 시, 유저들 offline로 초기화
def initialize_users():
    if not users:
        print("No users to initialize")
        return
    for user in users.values():
        user["status"] = status.Status.CHECKOUT.value
        user["reason"] = None
    print("Initialized all users to {}".format(status.Status.CHECKOUT.value))

# 유저 추가
def add_users(user_list: list[str]):
    for user_id in user_list:
        if user_id not in users:
            users[user_id] = {
                "status": status.Status.CHECKOUT.value,
                "reason": ""
            }
            print(f"Added user {user_id} with status {status.Status.CHECKOUT.value}")

# 입실(attendance) : 유저 상태 변경
def attendance_status(user_id: str):
    if user_id in users:
        users[user_id]["status"] = status.Status.ATTENDANCE.value
        print(f"Updated {user_id} to {status.Status.ATTENDANCE.value}")
        return
    print(f"User {user_id} not found")

# 퇴실(checkout) : 유저 상태 변경
def checkout_status(user_id: str):
    if user_id in users:
        users[user_id]["status"] = status.Status.CHECKOUT.value
        print(f"Updated {user_id} to {status.Status.CHECKOUT.value}")
        return
    print(f"User {user_id} not found")

# 자리비움(away) : 유저 상태 변경
# 자리비움은 출석(attendance)과 퇴실(checkout)과는 달리, 유저가 자리를 비운 상태를 나타냅니다.
# 자리비움 선택 후 이유를 작성할 시 해당 부분은 모두 알림으로 설정하여, 
# 자리비움 상태인 유저가 자리를 비운 이유를 다른 유저들이 알 수 있도록 하는 기능을 추가할 수 있습니다.    
def away_status(user_id: str, reason: str):
    if user_id not in users:
        print(f"User {user_id} not found")
        return
    elif users[user_id]["status"] != status.Status.ATTENDANCE.value:
        print(f"User {user_id} is not {status.Status.ATTENDANCE.value}, cannot set to away")
        return
    users[user_id]["status"] = status.Status.AWAY.value
    users[user_id]["reason"] = reason
    print(f"Updated {user_id} to {status.Status.AWAY.value} with reason: {reason}")

# 복귀(return) : 유저 상태 변경
def return_status(user_id: str):
    if user_id in users and users[user_id]["status"] == status.Status.AWAY.value:
        users[user_id]["status"] = status.Status.ATTENDANCE.value
        users[user_id]["reason"] = None
        print(f"Updated {user_id} to {status.Status.ATTENDANCE.value} from away")
        return
    print(f"User {user_id} not found or not in {status.Status.AWAY.value} status")

# 하루 작업 한 시간 계산
def calculate_work_time(user_id: str):
    # TODO : 유저들의 출석(attendance)과 퇴실(checkout) 시간을 기록하여,
    #  하루 작업 한 시간을 계산하는 기능 구현

    # pass는 아직 구현되지 않은 부분을 나타내는 키워드입니다.
    pass
