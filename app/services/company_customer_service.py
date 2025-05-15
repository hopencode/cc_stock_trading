from app.services.customer_service import Account
from app.methods.valid_check import *

class Company(Account):
    def __init__(self, db_manager):
        Account.__init__(self, db_manager)

    def set_role(self):
        self.db.execute("RESET ROLE")
        self.db.execute("SET ROLE mts_company")


    def dividend_payment(self):
        price, total_stock_count = self.db.execute("SELECT price, stock_num FROM company WHERE name = %s", (self.account_name,))[0]
        have_stock_count = self.db.execute("SELECT stock_count FROM company_balance WHERE a_number = %s AND stock_name = %s",
                                           (self.account_num, self.account_name))[0][0]
        sell_order_count = self.db.execute("SELECT count FROM order_list WHERE name = %s AND a_number = %s AND type = %s", (self.account_name, self.account_num, "sell"))
        if sell_order_count:
            for sell_order in sell_order_count:
                have_stock_count = have_stock_count + sell_order[0]

        customer_stock_count = total_stock_count - have_stock_count
        if customer_stock_count == 0:
            #print("100% 지분을 보유하고 있어 배당할 수 없습니다.")
            return  # 프론트 고민중

        valid_count = 0
        while True:
            dividend = input("주당 지급할 배당금을 입력하세요: ")
            dividend = int_valid_check(dividend)
            if dividend:
                break
            else:
                print("정수값으로 입력해주세요.")
                valid_count = valid_count + 1
                if valid_count == 5:
                    print("잘못된 값 5회 입력으로 메뉴로 돌아갑니다.")
                    return
                print()


        current_cash = self.current_cash()
        need_cash = customer_stock_count * dividend
        if current_cash < need_cash:
            print("배당금을 지급할 현금이 부족합니다.")
            return


        try:
            self.db.execute("UPDATE account SET cash = cash - %s WHERE a_number = %s", (need_cash, self.account_num))
            stock_have_customer = self.db.execute("SELECT a_number, stock_count FROM customer_balance WHERE stock_name = %s",
                                                  (self.account_name,))
            if stock_have_customer:
                for customer in stock_have_customer:
                    a_number = customer[0]
                    stock_count = customer[1]
                    add_cash = stock_count * dividend
                    self.db.execute("UPDATE account SET cash = cash + %s WHERE a_number = %s", (add_cash, a_number))

            stock_have_customer = self.db.execute("SELECT a_number, count FROM order_list WHERE name = %s AND type = %s AND a_number != %s",
                                                  (self.account_name, "sell", self.account_num))
            if stock_have_customer:
                for customer in stock_have_customer:
                    a_number = customer[0]
                    stock_count = customer[1]
                    add_cash = stock_count * dividend
                    self.db.execute("UPDATE account SET cash = cash + %s WHERE a_number = %s", (add_cash, a_number))
            self.db.conn.commit()
            print(f"주당 {dividend}씩 배당 완료")
        except Exception as e:
            self.db.conn.rollback()
            print(f"Error: {e}")