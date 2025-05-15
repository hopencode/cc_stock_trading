def string_valid_check(text, maxLenth):
    if len(text) > maxLenth:
        return None
    for i in text:
        if (i < '0' or i > '9') and (i < 'a' or i > 'z') and (i < 'A' or i > 'Z'):
            return None
    return True


def int_valid_check(value):
    try:
        value = int(value)
    except ValueError:
        return None
    else:
        return value

def float_valid_check(value):
    try:
        value = float(value)
    except ValueError:
        return None
    else:
        return value

def name_valid_check(text, maxLenth):
    if len(text) > maxLenth:
        return None
    for i in text:
        if (i < 'a' or i > 'z') and (i < 'A' or i > 'Z'):
            return None
    return True

def sector_valid_check(text, maxLenth):
    if len(text) > maxLenth:
        return None
    for i in text:
        if (i < 'a' or i > 'z') and (i < 'A' or i > 'Z') and (i != " "):
            return None
    return True


def input_name(text, lenth):
    valid_count = 0
    while True:
        name = input(f"{text} 입력: ")
        if name_valid_check(name, lenth):
            return name
        else:
            print("잘못된 입력입니다.")
            print("20자 이내의 알파벳으로 입력하세요.")
            valid_count = valid_count + 1
            if valid_count == 5:
                print("잘못된 값 5회 입력으로 메뉴로 돌아갑니다.")
                return None
            print()


def input_year():
    valid_count = 0
    while True:
        year = input("연도 입력: ")
        year = int_valid_check(year)
        if year != None:
            if year >= 1900 and year <= 9999:
                return year
            else:
                print("잘못된 입력입니다.")
                print("1900 ~ 9999 사이의 값만 유효합니다.")
                valid_count = valid_count + 1
                if valid_count == 5:
                    print("잘못된 값 5회 입력으로 메뉴로 돌아갑니다.")
                    return None
                print()
        else:
            print("잘못된 입력입니다.")
            valid_count = valid_count + 1
            if valid_count == 5:
                print("잘못된 값 5회 입력으로 메뉴로 돌아갑니다.")
                return None
            print()

def input_positive_int(text):
    valid_count = 0
    while True:
        value = input(f"{text} 입력: ")
        value = int_valid_check(value)
        if value != None and value >= 0:
            return value
        else:
            print("잘못된 입력입니다.")
            print("0 이상의 정수 형태로 값을 입력해주세요.")
            valid_count = valid_count + 1
            if valid_count == 5:
                print("잘못된 값 5회 입력으로 메뉴로 돌아갑니다.")
                return None
            print()


def input_natural_number(text):
    valid_count = 0
    while True:
        value = input(f"{text} 입력: ")
        value = int_valid_check(value)
        if value != None and value > 0:
            return value
        else:
            print("잘못된 입력입니다.")
            print("1 이상의 정수 형태로 값을 입력해주세요.")
            valid_count = valid_count + 1
            if valid_count == 5:
                print("잘못된 값 5회 입력으로 메뉴로 돌아갑니다.")
                return None
            print()

def input_int(text):
    valid_count = 0
    while True:
        value = input(f"{text} 입력: ")
        value = int_valid_check(value)
        if value != None:
            return value
        else:
            print("잘못된 입력입니다.")
            print("정수 형태로 값을 입력해주세요.")
            valid_count = valid_count + 1
            if valid_count == 5:
                print("잘못된 값 5회 입력으로 메뉴로 돌아갑니다.")
                return None
            print()

def input_float(text):
    valid_count = 0
    while True:
        value = input(f"{text} 입력: ")
        value = float_valid_check(value)
        if value != None:
            return value
        else:
            print("잘못된 입력입니다.")
            print("실수 형태로 값을 입력해주세요.")
            valid_count = valid_count + 1
            if valid_count == 5:
                print("잘못된 값 5회 입력으로 메뉴로 돌아갑니다.")
                return None
            print()

def register_id(db, type):
    if type == "admin":
        table = "admin"
    else:
        table = "account"
    valid_count = 0
    while True:
        id = input("생성할 계정의 ID를 입력하세요(알파벳, 숫자 조합 10자 이내): ")
        if string_valid_check(id, 10):
            sql = "SELECT * FROM " + table + " WHERE id = %s"
            current_id = db.execute(sql, (id,))
            if current_id:
                print("이미 등록된 ID입니다.")
                valid_count = valid_count + 1
                if valid_count == 5:
                    print("잘못된 값 5회 입력으로 메뉴로 돌아갑니다.")
                    return None
                print()
            else:
                print("사용 가능한 ID입니다.")
                return id
        else:
            print("유효하지 않은 ID입니다. (알파벳, 숫자 조합 10자 이내)")
            valid_count = valid_count + 1
            if valid_count == 5:
                print("잘못된 값 5회 입력으로 메뉴로 돌아갑니다.")
                return None
            print()



def register_password():
    valid_count = 0
    while True:
        password = input("생성할 계정의 비밀번호를 입력하세요(알파벳, 숫자 조합 12자 이내): ")
        if string_valid_check(password, 12):
            return password
        else:
            print("유효하지 않은 비밀번호입니다. (알파벳, 숫자 조합 12자 이내)")
            valid_count = valid_count + 1
            if valid_count == 5:
                print("잘못된 값 5회 입력으로 메뉴로 돌아갑니다.")
                return None
            print()


def register_name():
    valid_count = 0
    while True:
        name = input("이름을 입력하세요(알파벳 20자 이내): ")
        if name_valid_check(name, 20):
            return name
        else:
            print("유효하지 않은 이름입니다. (알파벳 20자 이내)")
            valid_count = valid_count + 1
            if valid_count == 5:
                print("잘못된 값 5회 입력으로 메뉴로 돌아갑니다.")
                return None
            print()


def register_phone():
    valid_count = 0
    while True:
        phone = input("전화번호를 입력하세요(-을 제외한 010으로 시작하는 11자리 숫자로 입력하세요): ")
        if len(phone) != 11:
            print("유효하지 않은 길이입니다. (-을 제외한 11자리 숫자로 입력하세요)")
            valid_count = valid_count + 1
            if valid_count == 5:
                print("잘못된 값 5회 입력으로 메뉴로 돌아갑니다.")
                return None
            print()
        else:
            if phone[:3] != "010":
                print("010으로 시작하는 11자리 숫자로 입력하세요")
                valid_count = valid_count + 1
                if valid_count == 5:
                    print("잘못된 값 5회 입력으로 메뉴로 돌아갑니다.")
                    return None
                print()
                continue
            else:
                valid = True
                for i in phone:
                    if i < '0' or i > '9':
                        print("-을 제외한 숫자로만 입력하세요")
                        valid_count = valid_count + 1
                        if valid_count == 5:
                            print("잘못된 값 5회 입력으로 메뉴로 돌아갑니다.")
                            return None
                        print()
                        valid = False
                        break
                if valid:
                    phone = phone[:3] + '-' + phone[3:7] + '-' + phone[7:]
                    return phone
                # else:
                # continue


def login_id():
    valid_count = 0
    while True:
        id = input("로그인할 계정의 ID를 입력하세요(알파벳, 숫자 조합 10자 이내): ")
        if string_valid_check(id, 10):
            return id
        else:
            print("유효하지 않은 ID입니다. (알파벳, 숫자 조합 10자 이내)")
            valid_count = valid_count + 1
            if valid_count == 5:
                print("잘못된 값 5회 입력으로 메뉴로 돌아갑니다.")
                return None
            print()

def login_password():
    valid_count = 0
    while True:
        password = input("비밀번호를 입력하세요(알파벳, 숫자 조합 12자 이내): ")
        if string_valid_check(password, 12):
            return password
        else:
            print("유효하지 않은 비밀번호입니다. (알파벳, 숫자 조합 12자 이내)")
            valid_count = valid_count + 1
            if valid_count == 5:
                print("잘못된 값 5회 입력으로 메뉴로 돌아갑니다.")
                return None
            print()