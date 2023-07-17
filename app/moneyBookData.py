class User:
    boardNum = []
    date = []
    profitOrSpending = []
    category = []
    price = []
    etc = []

    # 자바의 생성자 == __init--, self == this
    def __init__(self, boardNum, date, pos, category, price, etc):
        self.boardNum = boardNum
        self.date = date
        self.profitOrSpending = pos
        self.category = category
        self.price = price
        self.etc = etc

    def getBoardNum(self):
        return self.boardNum

    def setBoardNum(self, boardNum):
        self.boardNum = boardNum

    def getDate(self):
        return self.date

    def setDate(self, date):
        self.date = date

    def getProfitOrSpending(self):
        return self.profitOrSpending

    def setProfitOrSpending(self, profitOrSpending):
        self.profitOrSpending = profitOrSpending

    def getCategory(self):
        return self.category

    def setCategory(self, category):
        self.category = category

    def getPrice(self):
        return self.price

    def setPrice(self, price):
        self.price = price

    def getEtc(self):
        return self.etc

    def setEtc(self, etc):
        self.etc = etc
