from app.services.customer_service import Account

class Customer(Account):
    def __init__(self, db_manager):
        Account.__init__(self, db_manager)

    def set_role(self):
        self.db.execute("RESET ROLE")
        self.db.execute("SET ROLE mts_customer")

    def portfolio_weight_inquiry(self):
        sql = "SELECT c.sector, SUM(ba.stock_count * c.price) AS valuation_amount FROM customer_balance ba JOIN company c ON ba.stock_name = c.name WHERE ba.a_number = %s GROUP BY c.sector"
        #print(f"{self.account_name}님의 보유 주식 섹터별 비중")
        balance = self.db.execute(sql, (self.account_num, ))
        total_amount = 0
        portfolio_weight = []
        if balance:
            for stock in balance:
                total_amount = total_amount + stock[1]
            for stock in balance:
                weight = round(stock[1] / total_amount * 100, 2)
                weight = str(weight) + "%"
                sector = stock[0]
                portfolio_weight.append([sector, weight])
            #headers = ["Sector", "Weight"]
            #print(tabulate(portfolio_weight, headers=headers, tablefmt="fancy_grid"))
            return  # 프론트 고민중
        else:
            print("보유하고 있는 주식이 없습니다.")
            return # 프론트 고민중