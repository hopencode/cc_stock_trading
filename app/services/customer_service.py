import random
from datetime import datetime

from app.methods.valid_check import *

class Account:
    def __init__(self, db_manager):
        self.db = db_manager
        self.account_id = ""
        self.account_type = ""
        self.account_name = ""
        self.account_num = ""


    def register(self, type):
        account_type = type
        name = register_name()
        if name == None:
            return
        # name 중복 검사 (company만 해당)
        if account_type == "company":
            name = name.lower().capitalize()
            name_check = self.db.execute("SELECT name FROM company WHERE name = %s", (name, ))
            if not name_check:
                print("상장 기업 목록에 없는 기업입니다.")
                return
            name_check = self.db.execute("SELECT name FROM account WHERE type = %s AND name = %s", (account_type, name))
            if name_check:
                print("이미 계정이 존재하는 기업입니다.")
                return

        account_id = register_id(self.db, type)
        if account_id == None:
            return
        password = register_password()
        if password == None:
            return
        phone = register_phone()
        if phone == None:
            return

        valid_count = 0
        while True:
            a_number = random.randint(10000000, 99999999)
            current_a_numbers = self.db.execute("SELECT a_number FROM account WHERE a_number = %s", (a_number, ))
            if current_a_numbers:
                valid_count = valid_count + 1
                # 랜덤 10번 실패하면 사용중인 번호 제외하고 랜덤하고 뽑기
                if valid_count == 10:
                    exclude_list = []
                    current_a_numbers = self.db.execute("SELECT a_number FROM account")
                    for current_number in current_a_numbers:
                        exclude_list.append(current_number[0])
                    all_8digit_numbers = set(range(10000000, 100000000))
                    exclude_set = set(exclude_list)
                    possible_numbers = list(all_8digit_numbers - exclude_set)
                    if not possible_numbers:
                        print("유효한 계좌번호를 모두 사용중입니다.")
                        return
                    a_number = random.choice(possible_numbers)
                    break
                continue
            else:
                break

        # 계정 생성
        if account_type == "customer":
            try:
                self.db.execute( "INSERT INTO account (id, password, a_number, type, name, phone, cash, capital_gain) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                                 (account_id, password, a_number, account_type, name, phone, "0", "0"))
                self.db.conn.commit()
                print("계정 생성 성공")
            except Exception as e:
                self.db.conn.rollback()
                print(f"Error: {e}")
        else:
            now = datetime.now()
            current_date = now.date()
            current_time = now.time()

            buy_list_number = self.db.execute("SELECT MAX(buy_list_number) FROM buy_list")[0][0]
            if buy_list_number == None:
                buy_list_number = 1
            else:
                buy_list_number = buy_list_number + 1

            stock_price, stock_num = self.db.execute("SELECT price, stock_num FROM company WHERE name = %s", (name, ))[0]

            try:
                self.db.execute("INSERT INTO account (id, password, a_number, type, name, phone, cash, capital_gain) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                                (account_id, password, a_number, account_type, name, phone, 0, 0))
                self.db.execute("INSERT INTO buy_list (buy_list_number, a_number, name, price, b_date, b_time, b_count, s_count) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                                (buy_list_number, a_number, name, stock_price, current_date, current_time, stock_num, 0))
                self.db.execute("INSERT INTO company_balance (a_number, stock_name, stock_count, avg_buy_price) VALUES (%s, %s, %s, %s)",
                                (a_number, name, stock_num, stock_price))
                self.db.conn.commit()
                print("계정 생성 성공")
            except Exception as e:
                self.db.conn.rollback()
                print(f"Error: {e}")


    def login(self):
        valid_count = 0
        account_id = login_id()
        global systemRun
        while True:
            password = login_password()
            existent_id = self.db.execute("SELECT id FROM account WHERE id = %s", (account_id, ))
            if existent_id:
                login_result = self.db.execute("SELECT id, type, name, a_number FROM account WHERE id = %s AND password = %s", (account_id, password))
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
        self.account_id = login_result[0][0]
        self.account_type = login_result[0][1]
        self.account_name = login_result[0][2]
        self.account_num = login_result[0][3]
        return login_result


    def current_cash(self):
        cash = self.db.execute("SELECT cash FROM account WHERE a_number = %s", (self.account_num,))[0][0]
        #print(f"잔액: {cash}")
        return cash

    def deposit(self):
        amount = input_positive_int("입금할 금액")
        if amount == None:
            return
        if amount == 0:
            print("잔액의 변동이 없습니다.")
            return
        try:
            self.db.execute("UPDATE account SET cash = cash + %s WHERE id = %s", (amount, self.account_id))
            self.db.conn.commit()
            print(f"{amount}원 입금 완료")
            cash = self.current_cash()
            print(f"잔액: {cash}")
            print()
        except Exception as e:
            self.db.conn.rollback()
            print(f"Error: {e}")

    def withdrawal(self):
        amount = input_positive_int("출금할 금액")
        if amount == None:
            return
        if amount == 0:
            print("잔액의 변동이 없습니다.")
            return
        cash = self.db.execute("SELECT cash FROM account WHERE id = %s", (self.account_id,))[0][0]
        if cash < amount:
            print("잔액이 부족합니다")
            return

        try:
            self.db.execute("UPDATE account SET cash = cash - %s WHERE id = %s", (amount, self.account_id))
            self.db.conn.commit()
            print(f"{amount}원 출금 완료")
            cash = self.current_cash()
            print(f"잔액: {cash}")
            print()
        except Exception as e:
            self.db.conn.rollback()
            print(f"Error: {e}")

    def show_company_list(self):
        companys = self.db.execute("SELECT name, price, stock_num FROM company")
        if len(companys) == 0:
            print("상장된 기업이 없습니다.")
            print()
            return
        try:
            for company in companys:
                name, price, stock_num = company
                self.db.execute("UPDATE company SET total_price = %s WHERE name = %s", (price * stock_num, name))
            self.db.conn.commit()
        except Exception as e:
            self.db.conn.rollback()
            print(f"Error: {e}")
            return
        companys = self.db.execute(
            "SELECT name, price, stock_num, total_price, sector FROM company ORDER BY total_price DESC")

        print("상장 기업 목록")
        headers = ["Name", "Stock Price", "Stock Num", "Total Price", "Sector"]
        print(tabulate(companys, headers=headers, tablefmt="fancy_grid"))
        print()

    def show_company_info(self):
        name = input_name("정보를 확인할 기업의 이름", 20)
        if name == None:
            return
        name = name.lower().capitalize()
        company_list = self.db.execute("SELECT * FROM company WHERE name = %s", (name, ))
        if len(company_list) == 0:
            print("상장 기업 목록에 없는 기업 이름입니다.")
            print("상장 기업 목록의 이름을 정확히 입력하세요 (대소문자 구분X)")
            return

        financial_info = self.db.execute("SELECT year, sales, business_profits, pure_profits, EPS, BPS, PER, PBR FROM financial_info WHERE name = %s ORDER BY year DESC",
                                         (name,))
        if len(financial_info) == 0:
            print("등록된 재무정보가 없습니다.")
            return
        print()
        print(f"{name}의 재무제표")
        headers = ["Year", "Sales", "Business Profits", "Pure Profits", "EPS", "BPS", "PER", "PBR"]
        print(tabulate(financial_info, headers=headers, tablefmt="fancy_grid"))


    def show_company_order(self):
        if self.account_type == "company":
            name = self.account_name
        else:
            name = input_name("주문을 확인할 기업의 이름", 20)
            if name == None:
                return
            name = name.lower().capitalize()

            company_list = self.db.execute("SELECT * FROM company WHERE name = %s", (name,))
            if len(company_list) == 0:
                print("상장 기업 목록에 없는 기업 이름입니다.")
                print("상장 기업 목록의 이름을 정확히 입력하세요 (대소문자 구분X)")
                return

        company_buy_order_list = self.db.execute("SELECT price, count, type FROM order_list WHERE name = %s AND type = %s ORDER BY price DESC", (name, "buy"))
        company_sell_order_list = self.db.execute("SELECT price, count, type FROM order_list WHERE name = %s AND type = %s ORDER BY price DESC", (name, "sell"))

        if len(company_buy_order_list) == 0 and len(company_sell_order_list) == 0:
            print(f"{name} 기업에 대해 등록된 주문이 없습니다.")
            return

        if len(company_sell_order_list) > 0:
            print()
            print(f"{name} 매도 호가창")
            headers = ["Price", "Count", "Type"]
            print(tabulate(company_sell_order_list, headers=headers, tablefmt="fancy_grid"))
            if len(company_buy_order_list) > 0 and len(company_sell_order_list) > 0:
                print("--------------------------")

        if len(company_buy_order_list) > 0:
            print(f"{name} 매수 호가창")
            headers = ["Price", "Count", "Type"]
            print(tabulate(company_buy_order_list, headers=headers, tablefmt="fancy_grid"))
            print()



    def register_buy_order(self, name, price, count, order_number):
        self.db.execute("INSERT INTO order_list (a_number, type, name, price, count, order_number) VALUES (%s, %s, %s, %s, %s, %s)",
                        (self.account_num, "buy", name, price, count, order_number))

    def register_sell_order(self, name, price, count, order_number):
        self.db.execute("INSERT INTO order_list (a_number, type, name, price, count, order_number) VALUES (%s, %s, %s, %s, %s, %s)",
                        (self.account_num, "sell", name, price, count, order_number))

    def buy_contract_conclusion(self, a_number, name, price, count):
        a_type = self.db.execute("SELECT type FROM account WHERE a_number = %s", (a_number, ))[0][0]
        current_stock_price = self.db.execute("SELECT price FROM company WHERE name = %s", (name,))[0][0]

        if a_type == "customer":
            present_stock = self.db.execute("SELECT stock_count, avg_buy_price FROM customer_balance WHERE a_number = %s AND stock_name = %s",
                                            (a_number, name))
            if present_stock:
                stock_count = present_stock[0][0]
                avg_buy_price = present_stock[0][1]
                total_buy_price = stock_count * avg_buy_price + price * count

                avg_buy_price = total_buy_price / (stock_count + count)
                avg_buy_price = round(avg_buy_price, 2)

                sql = "UPDATE customer_balance SET stock_count = stock_count + %s, avg_buy_price = %s WHERE a_number = %s AND stock_name = %s"
            else:
                sql = "INSERT INTO customer_balance (a_number, stock_name, stock_count, avg_buy_price) VALUES (%s, %s, %s, %s)"
        else:
            present_stock = self.db.execute("SELECT stock_count, avg_buy_price FROM company_balance WHERE a_number = %s AND stock_name = %s",
                                            (a_number, name))
            if present_stock:
                stock_count = present_stock[0][0]
                avg_buy_price = present_stock[0][1]
                total_buy_price = stock_count * avg_buy_price + price * count

                avg_buy_price = total_buy_price / (stock_count + count)
                avg_buy_price = round(avg_buy_price, 2)

                sql = "UPDATE company_balance SET stock_count = stock_count + %s, avg_buy_price = %s WHERE a_number = %s AND stock_name = %s"
            else:
                sql = "INSERT INTO company_balance (a_number, stock_name, stock_count, avg_buy_price) VALUES (%s, %s, %s, %s)"

        now = datetime.now()
        current_date = now.date()
        current_time = now.time()

        buy_list_number = self.db.execute("SELECT MAX(buy_list_number) FROM buy_list")[0][0]
        if buy_list_number == None:
            buy_list_number = 1
        else:
            buy_list_number = buy_list_number + 1
        self.db.execute("INSERT INTO buy_list (buy_list_number, a_number, name, price, b_date, b_time, b_count, s_count) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                        (buy_list_number, a_number, name, price, current_date, current_time, count, 0))
        if present_stock:
            self.db.execute(sql, (count, avg_buy_price, a_number, name))
        else:
            self.db.execute(sql, (a_number, name, count, price))



    def sell_contract_conclusion(self, a_number, name, price, count):
        buy_contract = self.db.execute("SELECT buy_list_number, price, b_date, b_time, b_count, s_count FROM buy_list WHERE a_number = %s AND name = %s AND b_count > s_count ORDER BY b_date ASC, b_time ASC",
                                       (a_number, name))
        if buy_contract:
            now = datetime.now()
            current_date = now.date()
            current_time = now.time()
            cash = price * count
            sell_list_number = self.db.execute("SELECT MAX(sell_list_number) FROM sell_list")[0][0]
            if sell_list_number == None:
                sell_list_number = 0

            for contract in buy_contract:
                buy_list_number, b_price, b_date, b_time, b_count, s_count = contract
                stock_count = b_count - s_count
                capital_gain = price - b_price
                if count >= stock_count:
                    self.db.execute("UPDATE buy_list SET s_count = s_count + %s WHERE a_number = %s AND name = %s AND b_date = %s AND b_time = %s AND buy_list_number = %s",
                                    (stock_count, a_number, name, b_date, b_time, buy_list_number))
                    count = count - stock_count
                    order_count = stock_count
                else:
                    self.db.execute("UPDATE buy_list SET s_count = s_count + %s WHERE a_number = %s AND name = %s AND b_date = %s AND b_time = %s AND buy_list_number = %s",
                                    (count, a_number, name, b_date, b_time, buy_list_number))
                    order_count = count
                    count = 0
                sell_list_number = sell_list_number + 1
                self.db.execute("INSERT INTO sell_list (sell_list_number, a_number, name, b_price, s_price, s_date, s_time, s_count) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                                (sell_list_number, a_number, name, b_price, price, current_date, current_time, order_count))
                self.db.execute("UPDATE account SET capital_gain = capital_gain + %s WHERE a_number = %s", (capital_gain * order_count, a_number))
                if count == 0:
                    break
            self.db.execute("UPDATE account SET cash = cash + %s WHERE a_number = %s", (cash, a_number))

            account_type = self.db.execute("SELECT type FROM account WHERE a_number = %s", (a_number, ))[0][0]
            if account_type == "customer":
                after_conclusion_stock_count = self.db.execute("SELECT stock_count FROM customer_balance WHERE a_number = %s AND stock_name = %s",
                                                               (a_number, name))[0][0]
                remain_sell_order = self.db.execute("SELECT * FROM order_list WHERE a_number = %s AND type = %s AND name = %s",
                                                    (a_number, "sell", name))
                if after_conclusion_stock_count == 0 and len(remain_sell_order) == 0:
                    self.db.execute("DELETE FROM customer_balance WHERE a_number = %s AND stock_name = %s",
                                    (a_number, name))
            else:
                after_conclusion_stock_count = self.db.execute("SELECT stock_count FROM company_balance WHERE a_number = %s AND stock_name = %s",
                                                               (a_number, name))[0][0]
                remain_sell_order = self.db.execute( "SELECT * FROM order_list WHERE a_number = %s AND type = %s AND name = %s",
                                                     (a_number, "sell", name))
                if after_conclusion_stock_count == 0 and len(remain_sell_order) == 0:
                    self.db.execute("DELETE FROM company_balance WHERE a_number = %s AND stock_name = %s",
                                    (a_number, name))
        else:
            print("매도 가능한 매수체결 기록이 없음")
            return


    def buy(self):
        if self.account_type == "customer":
            name = input_name("매수할 기업의 이름", 20)
            if name == None:
                return
            name = name.lower().capitalize()
            company_list = self.db.execute("SELECT * FROM company WHERE name = %s", (name,))
            if len(company_list) == 0:
                print("상장 기업 목록에 없는 기업입니다.")
                return
        else:
            name = self.account_name
        price = input("주당 매수 가격을 입력하세요: ")
        price = int_valid_check(price)
        if price == None or price <= 0:
            print("잘못된 입력입니다.")
            print("매수 가격은 1 이상의 정수값으로 입력해주세요.")
            return
        order_count = input("매수할 개수를 입력하세요: ")
        order_count = int_valid_check(order_count)
        if order_count == None or order_count <= 0:
            print("잘못된 입력입니다.")
            print("매수 수량은 1 이상의 정수값으로 입력해주세요.")
            return

        count = order_count
        cash = price * order_count
        current_cash = self.current_cash()
        if cash > current_cash:
            print("잔액이 부족합니다.")
            print()
            return

        current_max_order_number = self.db.execute("SELECT MAX(order_number) FROM order_list")
        if current_max_order_number[0][0] == None:
            order_number = 1
        else:
            order_number = current_max_order_number[0][0] + 1

        present_sell_order = self.db.execute("SELECT a_number, count, order_number FROM order_list WHERE name = %s AND type = %s AND price = %s AND a_number != %s ORDER BY order_number",
                                     (name, "sell", price, self.account_num))
        if present_sell_order:
            try:
                self.db.execute("UPDATE account SET cash = cash - %s WHERE a_number = %s", (cash, self.account_num))
                for contract in present_sell_order:
                    a_number, sell_order_count, sell_order_number = contract
                    if count >= sell_order_count:
                        self.db.execute("DELETE FROM order_list WHERE order_number = %s", (sell_order_number,))
                        self.sell_contract_conclusion(a_number, name, price, sell_order_count)
                        count = count - sell_order_count
                    else:
                        self.db.execute("UPDATE order_list SET count = count - %s WHERE a_number = %s AND order_number = %s",
                                        (count, a_number, sell_order_number))
                        self.sell_contract_conclusion(a_number, name, price, count)
                        count = 0
                    if count == 0:
                        break
                if count > 0:
                    self.register_buy_order(name, price, count, order_number)
                conclusion_count = order_count - count
                self.buy_contract_conclusion(self.account_num, name, price, conclusion_count)
                self.db.execute("UPDATE company SET price = %s WHERE name = %s", (price, name))
                self.db.conn.commit()
                print(f"주문번호 {order_number}번 매수 주문 완료")
                print(f"{conclusion_count}주는 매수 주문 체결")
                print(f"미체결 잔여 물량: {count}주")
            except Exception as e:
                self.db.conn.rollback()
                print(f"Error: {e}")
        else:
            try:
                self.db.execute("UPDATE account SET cash = cash - %s WHERE a_number = %s", (cash, self.account_num))
                self.register_buy_order(name, price, order_count, order_number)
                self.db.conn.commit()
                print(f"주문번호 {order_number}번 매수 주문 완료")
            except Exception as e:
                self.db.conn.rollback()
                print(f"Error: {e}")


    def sell(self):
        if self.account_type == "customer":
            name = input_name("매도할 기업의 이름", 20)
            if name == None:
                return
            name = name.lower().capitalize()
            current_stock = self.db.execute("SELECT stock_count FROM customer_balance WHERE a_number = %s AND stock_name = %s", (self.account_num, name))
        else:
            name = self.account_name
            current_stock = self.db.execute("SELECT stock_count FROM company_balance WHERE a_number = %s AND stock_name = %s", (self.account_num, self.account_name))

        if len(current_stock) == 0:
            print("해당 주식을 보유하고 있지 않습니다.")
            return

        price = input("주당 매도 가격을 입력하세요: ")
        price = int_valid_check(price)
        if price == None or price <= 0:
            print("잘못된 입력입니다.")
            print("매도 가격은 1 이상의 정수값으로 입력해주세요.")
            return
        order_count = input("매도할 개수를 입력하세요: ")
        order_count = int_valid_check(order_count)
        if order_count == None or order_count <= 0:
            print("잘못된 입력입니다.")
            print("매도 수량은 1 이상의 정수값으로 입력해주세요.")
            return
        count = order_count
        stock_count = current_stock[0][0]
        if stock_count < order_count:
            print("보유 주식이 부족합니다.")
            return

        current_max_order_number = self.db.execute("SELECT MAX(order_number) FROM order_list")
        if current_max_order_number[0][0] == None:
            order_number = 1
        else:
            order_number = current_max_order_number[0][0] + 1

        present_buy_order = self.db.execute("SELECT a_number, count, order_number FROM order_list WHERE name = %s AND type = %s AND price = %s AND a_number != %s  ORDER BY order_number",
                                            (name, "buy", price, self.account_num))

        if present_buy_order:
            try:
                if self.account_type == "customer":
                    self.db.execute("UPDATE customer_balance SET stock_count = stock_count - %s WHERE a_number = %s AND stock_name = %s",
                                    (order_count, self.account_num, name))
                else:
                    self.db.execute("UPDATE company_balance SET stock_count = stock_count - %s WHERE a_number = %s AND stock_name = %s",
                                    (order_count, self.account_num, name))
                for contract in present_buy_order:
                    a_number, buy_order_count, buy_order_number = contract
                    if count >= buy_order_count:
                        self.db.execute("DELETE FROM order_list WHERE order_number = %s", (buy_order_number,))
                        self.buy_contract_conclusion(a_number, name, price, buy_order_count)
                        count = count - buy_order_count
                    else:
                        self.db.execute("UPDATE order_list SET count = count - %s WHERE a_number = %s AND order_number = %s",
                                        (count, a_number, buy_order_number))
                        self.buy_contract_conclusion(a_number, name, price, count)
                        count = 0
                        break
                if count > 0:
                    self.register_sell_order(name, price, count, order_number)

                conclusion_count = order_count - count
                self.sell_contract_conclusion(self.account_num, name, price, conclusion_count)
                self.db.execute("UPDATE company SET price = %s WHERE name = %s", (price, name))
                self.db.conn.commit()
                print(f"주문번호 {order_number}번 매도 주문 완료")
                print(f"{conclusion_count}주는 매도 주문 체결")
                print(f"미체결 잔여 물량: {count}주")
            except Exception as e:
                self.db.conn.rollback()
                print(f"Error: {e}")
        else:
            try:
                if self.account_type == "customer":
                    self.db.execute("UPDATE customer_balance SET stock_count = stock_count - %s WHERE a_number = %s AND stock_name = %s", (order_count, self.account_num, name))
                else:
                    self.db.execute("UPDATE company_balance SET stock_count = stock_count - %s WHERE a_number = %s AND stock_name = %s", (order_count, self.account_num, name))
                self.register_sell_order(name, price, order_count, order_number)
                self.db.conn.commit()
                print(f"주문번호 {order_number}번 매도 주문 완료")
            except Exception as e:
                self.db.conn.rollback()
                print(f"Error: {e}")

    def show_order_list(self):
        order_list = self.db.execute("SELECT name, type, price, count, order_number FROM order_list WHERE a_number = %s",
                                     (self.account_num,))
        if order_list:
            headers = ["Company", "Type", "Price", "Count", "order_number"]
            print(tabulate(order_list, headers=headers, tablefmt="fancy_grid"))
        else:
            print("체결되지 않은 주문이 없습니다.")

    def cancel_order(self):
        order_number = input_natural_number("취소할 주문의 주문번호")
        if order_number == None:
            return
        current_order_info = self.db.execute("SELECT name, type, price, count FROM order_list WHERE order_number = %s AND a_number = %s",
                                     (order_number, self.account_num))

        if current_order_info:
            name, type, price, count = current_order_info[0]
            if type == "buy":
                cash = price * count
                try:
                    self.db.execute("DELETE FROM order_list WHERE order_number = %s", (order_number,))
                    self.db.execute("UPDATE account SET cash = cash + %s WHERE a_number = %s", (cash, self.account_num))
                    self.db.conn.commit()
                    print(f"주문번호 {order_number}번 취소 완료")
                except Exception as e:
                    self.db.conn.rollback()
                    print(f"Error: {e}")
            else:  # sell order cancel
                if self.account_type == "customer":
                    update_stock_count_sql = "UPDATE customer_balance SET stock_count = stock_count + %s WHERE a_number = %s and stock_name = %s"
                else:
                    update_stock_count_sql = "UPDATE company_balance SET stock_count = stock_count + %s WHERE a_number = %s and stock_name = %s"
                try:
                    self.db.execute("DELETE FROM order_list WHERE order_number = %s", (order_number,))
                    self.db.execute(update_stock_count_sql, (count, self.account_num, name))
                    self.db.conn.commit()
                    print(f"주문번호 {order_number}번 취소 완료")
                except Exception as e:
                    self.db.conn.rollback()
                    print(f"Error: {e}")
        else:
            print("해당 계좌의 주문 내역 중 해당하는 번호의 주문이 없습니다.")

    def show_balance_inquiry(self):
        account_info = self.db.execute("SELECT cash, capital_gain FROM account WHERE a_number = %s",
                                       (self.account_num,))[0]

        if self.account_type == "customer":
            balance = self.db.execute("SELECT stock_name, stock_count, avg_buy_price FROM customer_balance WHERE a_number = %s",
                                      (self.account_num,))
        else:
            balance = self.db.execute("SELECT stock_name, stock_count, avg_buy_price FROM company_balance WHERE a_number = %s",
                                      (self.account_num,))

        print(f"{self.account_name}님의 계좌 잔고")
        print(f"현금: {account_info[0]}, 누적 양도 소득: {account_info[1]}")
        if balance:
            for i in range(len(balance)):
                temp = list(balance[i])
                price = self.db.execute("SELECT price FROM company WHERE name = %s", (balance[i][0],))[0][0]
                valuation_amount = price * balance[i][1]
                temp.append(valuation_amount)
                balance[i] = temp
            headers = ["Stock", "Count", "Avg Buy Price", "Valuation Amount"]
            print(tabulate(balance, headers=headers, tablefmt="fancy_grid"))
        else:
            print("보유하고 있는 주식이 없습니다.")