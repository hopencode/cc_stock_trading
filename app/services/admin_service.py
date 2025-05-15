from app.methods.valid_check import *

class Admin:
    def __init__(self, db_manager):
        self.db = db_manager
        self.admin_id = ""
        self.type = "admin"


    def set_role(self):
        self.db.execute("RESET ROLE")
        self.db.execute("SET ROLE mts_admin")

    def register(self):
        admin_id = register_id(self.db, self.type)
        if admin_id == None:
            return
        password = register_password()
        if password == None:
            return

        try:
            self.db.execute("INSERT INTO admin (id, password, type) VALUES (%s, %s, %s)", (admin_id, password, self.type))
            self.db.conn.commit()
            print("계정 생성 성공")
        except Exception as e:
            self.db.conn.rollback()
            print(f"Error: {e}")

    def login(self):
        valid_count = 0
        admin_id = login_id()
        global systemRun
        while True:
            password = login_password()
            existent_id = self.db.execute("SELECT id FROM admin WHERE id = %s", (admin_id, ))
            if existent_id:
                login_result = self.db.execute("SELECT id FROM admin WHERE id = %s AND password = %s", (admin_id, password))
                if login_result:
                    break
                else:
                    print("비밀번호가 틀렸습니다.")
                    valid_count = valid_count + 1
                    if valid_count == 5:
                        systemRun = False
                        print("비밀번호가 5회 틀려 프로그램을 종료합니다.")
                        return None
                    print()
            else:
                print("존재하지 않는 ID입니다.")
                return None

        print(f"{login_result[0][0]} 계정 로그인 성공")
        self.admin_id = login_result[0][0]
        return login_result

    def show_company_list(self):
        companys = self.db.execute("SELECT name, price, stock_num FROM company")
        if len(companys) == 0:
            print("상장된 기업이 없습니다.")
            print()
            return
        try:
            for company in companys:
                name, price, stock_num = company
                self.db.execute("UPDATE company SET total_price = %s WHERE name = %s", (price*stock_num, name))
            self.db.conn.commit()
        except Exception as e:
            self.db.conn.rollback()
            print(f"Error: {e}")
            return
        companys = self.db.execute("SELECT name, price, stock_num, total_price, sector FROM company ORDER BY total_price DESC")

        print("상장 기업 목록")
        headers = ["Name", "Stock Price", "Stock Num", "Total Price", "Sector"]
        print(tabulate(companys, headers=headers, tablefmt="fancy_grid"))
        print()



    def update_sector(self):
        valid_count = 0
        while True:
            company_name = input("산업 분야를 수정할 기업 이름: ")
            if name_valid_check(company_name, 20):
                break
            else:
                valid_count = valid_count + 1
                if valid_count == 5:
                    print("잘못된 값 5회 입력으로 메뉴로 돌아갑니다.")
                    return
                print("잘못된 입력값입니다.")
                print("20자 이내의 알파벳으로 입력하세요.")
                print()

        company_name = company_name.lower().capitalize()
        present_company = self.db.execute("SELECT name FROM company WHERE name = %s", (company_name,))
        if len(present_company) == 0:
            print("상장 기업 목록에 없는 기업입니다.")
            return

        valid_count = 0
        while True:
            sector = input("산업 분야: ")
            if sector_valid_check(sector, 25):
                break
            else:
                valid_count = valid_count + 1
                if valid_count == 5:
                    print("잘못된 값 5회 입력으로 메뉴로 돌아갑니다.")
                    return
                print("잘못된 입력값입니다.")
                print("25자 이내의 알파벳으로 입력하세요.")
                print()
        try:
            self.db.execute("UPDATE company SET sector = %s WHERE name = %s", (sector, company_name))
            self.db.conn.commit()
            print(f"{company_name}의 Sector 수정: {sector}")
        except Exception as e:
            self.db.conn.rollback()
            print(f"Error: {e}")

    def register_company(self):
        valid_count = 0
        while True:
            company_name = input("상장할 기업 이름: ")
            if name_valid_check(company_name, 20):
                break
            else:
                valid_count = valid_count + 1
                if valid_count == 5:
                    print("잘못된 값 5회 입력으로 메뉴로 돌아갑니다.")
                    return
                print("잘못된 입력값입니다.")
                print("20자 이내의 알파벳으로 입력하세요.")
                print()

        present_company = self.db.execute("SELECT name FROM company WHERE name = %s", (company_name, ))
        if present_company:
            print("이미 등록된 기업입니다.")
            return

        company_name = company_name.lower().capitalize()
        valid_count = 0
        while True:
            stock_price = input("주식 주당 가격: ")
            stock_price = int_valid_check(stock_price)
            if stock_price and stock_price > 0:
                break
            else:
                valid_count = valid_count + 1
                if valid_count == 5:
                    print("잘못된 값 5회 입력으로 메뉴로 돌아갑니다.")
                    return
                print("잘못된 입력값입니다.")
                print("1 이상의 정수로 입력하세요.")
                print()

        valid_count = 0
        while True:
            stock_num = input("주식 수: ")
            stock_num = int_valid_check(stock_num)
            if stock_num and stock_num > 0:
                break
            else:
                valid_count = valid_count + 1
                if valid_count == 5:
                    print("잘못된 값 5회 입력으로 메뉴로 돌아갑니다.")
                    return
                print("잘못된 입력값입니다.")
                print("1 이상의 정수로 입력하세요.")
                print()

        valid_count = 0
        while True:
            sector = input("산업 분야: ")
            if sector_valid_check(sector, 25):
                break
            else:
                valid_count = valid_count + 1
                if valid_count == 5:
                    print("잘못된 값 5회 입력으로 메뉴로 돌아갑니다.")
                    return
                print("잘못된 입력값입니다.")
                print("25자 이내의 알파벳으로 입력하세요.")
                print()

        total_price = stock_price * stock_num
        try:
            self.db.execute("INSERT INTO company (name, price, stock_num, total_price, sector) VALUES (%s, %s, %s, %s, %s)",
                            (company_name, stock_price, stock_num, total_price, sector ))
            self.db.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print(f"Error: {e}")

