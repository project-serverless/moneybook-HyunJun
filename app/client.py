import datetime as dt
import pandas as pd

boardNum = []
date = []
profitOrSpending = []
category = []
price = []
etc = []

# 데이터 초기화
def initData():
    global boardNum
    global date
    global profitOrSpending
    global category
    global price
    global etc
    boardNum = []
    date = []
    profitOrSpending = []
    category = []
    price = []
    etc = []

# 데이터 추가(Create)
def createData():
    print("=============================== 데이터 입력 ==================================")
    inputDate = input("날짜 입력 : ")
    inputPos = input("수익/지출 입력 : ")
    inputCategory = input("카테고리 입력 : ")
    inputPrice = input("금액 입력 : ")
    inputEtc = input("기타 입력 : ")
    
    if(len(boardNum) == 0):
        boardNum.append(boardNum+1)
    else:
        boardNum.append(boardNum[-1]+1)
    date.append(inputDate)
    profitOrSpending.append(inputPos)
    category.append(inputCategory)
    price.append(inputPrice)
    etc.append(inputEtc)
    
    print("=============================== 데이터 저장 ==================================")
    df = pd.DataFrame(boardNum, columns=['boardNum'])
    df['date'] = date
    df['breakdown'] = profitOrSpending
    df['category'] = category
    df['price'] = price
    df['etc'] = etc
    df.to_csv("app/moneyBook.csv", index=False)

# 데이터 불러오기(Read)
def readCsvData(file_path):
    df = pd.read_csv(file_path)
    for row in df.itertuples(index=False):
        boardNum.append(row[0])
        date.append(row[1])
        profitOrSpending.append(row[2])
        category.append(row[3])
        price.append(row[4])
        etc.append(row[5])
    print(df)
    return df

# 데이터 수정(Update)
def modifyData():
    selectBoardNum = int(input("수정 할 거래번호 선택 : \n"))

    if selectBoardNum in boardNum:
        inputDate = input("날짜 입력 : ")
        inputPos = input("수익/지출 입력 : ")
        inputCategory = input("카테고리 입력 : ")
        inputPrice = input("금액 입력 : ")
        inputEtc = input("기타 입력 : ")

        date[boardNum.index(selectBoardNum)] = inputDate
        profitOrSpending[boardNum.index(selectBoardNum)] = inputPos
        category[boardNum.index(selectBoardNum)] = inputCategory
        price[boardNum.index(selectBoardNum)] = inputPrice
        etc[boardNum.index(selectBoardNum)] = inputEtc

        df = pd.DataFrame(boardNum, columns=['boardNum'])
        df['date'] = date
        df['breakdown'] = profitOrSpending
        df['category'] = category
        df['price'] = price
        df['etc'] = etc
        df.to_csv("app/moneyBook.csv", index=False)

    else:
        print("입력하신 거래번호가 존재하지 않습니다.")

# 데이터 삭제(Delete)
def deleteData(file_path):
    df = pd.read_csv(file_path)
    selectBoardNum = int(input("삭제 할 거래번호 선택 : \n"))
    dfDeleted = df.drop(df[df['boardNum'] == selectBoardNum].index)
    
    if selectBoardNum in boardNum:
        initData()
        for row in dfDeleted.itertuples(index=False):
            boardNum.append(row[0])
            date.append(row[1])
            profitOrSpending.append(row[2])
            category.append(row[3])
            price.append(row[4])
            etc.append(row[5])

        df = pd.DataFrame(boardNum, columns=['boardNum'])
        df['date'] = date
        df['breakdown'] = profitOrSpending
        df['category'] = category
        df['price'] = price
        df['etc'] = etc
        df.to_csv("app/moneyBook.csv", index=False)
        
    else:
        print("입력하신 거래번호가 존재하지 않습니다.")
        
def main():
    initData()
    print("=============================== 데이터 취득 ==================================")
    readCsvData(file_path='app/moneyBook.csv')
    print("============================================================================")
    selection = int(input("1. 데이터 저장 / 2. 데이터 불러오기 / 3. 데이터 수정 /4. 데이터 삭제 / 5. 종료\n"))
    # 데이터 저장
    if selection == 1:
        createData()

    # 데이터 불러오기
    elif selection == 2:
        readCsvData(file_path='app/moneyBook.csv')
 
    # 데이터 수정
    elif selection == 3:
        modifyData()

    # 데이터 삭제
    elif selection == 4:
        deleteData(file_path='app/moneyBook.csv')

    else:
        return 0
    
    main()
    

if __name__ == "__main__":
    main()