import datetime as dt
import pandas as pd
import moneyBookData

# 데이터 입력 클래스
class ControlData:
    #csv로부터 데이터 import
    def readCsvData(self, file_path, User):
        df = pd.read_csv(file_path) # index_col=0
        for row in df.itertuples(index=False):
            User.boardNum.append(row[0])
            User.date.append(row[1])
            User.profitOrSpending.append(row[2])
            User.category.append(row[3])
            User.price.append(row[4])
            User.etc.append(row[5])
        print(df)
        return df

    # 데이터 추가(Create)
    def createData(self, User):
        print("=============================== 데이터 입력 ==================================")
        date = input("날짜 입력 : ")
        pos = input("수익/지출 입력 : ")
        category = input("카테고리 입력 : ")
        price = input("금액 입력 : ")
        etc = input("기타 입력 : ")

        User.boardNum.append(User.boardNum[-1]+1)
        User.date.append(date)
        User.profitOrSpending.append(pos)
        User.category.append(category)
        User.price.append(price)
        User.etc.append(etc)

        # print("============================================================================")
        # print("boardNum=", User.boardNum)
        # print("date=", User.date)
        # print("profitOrSpending=", User.profitOrSpending)
        # print("category=", User.category)
        # print("price=", User.price)
        # print("etc=", User.etc)
        print("=============================== 데이터 저장 ==================================")
        df = pd.DataFrame(User.boardNum, columns=['boardNum'])
        df['date'] = User.date
        df['breakdown'] = User.profitOrSpending
        df['category'] = User.category
        df['price'] = User.price
        df['etc'] = User.etc

        df.to_csv("moneyBook.csv", index=False)

    # 데이터 불러오기(Read)
    def readAllData(self, User):
        User.getBoardNum(self=User)
        User.getDate(self=User)
        User.getProfitOrSpending(self=User)
        User.getCategory(self=User)
        User.getPrice(self=User)
        User.getEtc(self=User)

        # 출력 확인용
        # print(User.getBoardNum(self=User))
        # print(User.getDate(self=User))
        # print(User.getProfitOrSpending(self=User))
        # print(User.getCategory(self=User))
        # print(User.getPrice(self=User))
        # print(User.getEtc(self=User))
        #

    # 데이터 수정
    def modifyData(self ,ur):
        selectBoardNum = int(input("수정 할 거래번호 선택 : \n"))

        date = input("날짜 입력 : ")
        profitOrSpending = input("수익/지출 입력 : ")
        category = input("카테고리 입력 : ")
        price = input("금액 입력 : ")
        etc = input("기타 입력 : ")

        ur.date[ur.boardNum.index(selectBoardNum)] = date
        ur.profitOrSpending[ur.boardNum.index(selectBoardNum)] = profitOrSpending
        ur.category[ur.boardNum.index(selectBoardNum)] = category
        ur.price[ur.boardNum.index(selectBoardNum)] = price
        ur.etc[ur.boardNum.index(selectBoardNum)] = etc

        df = pd.DataFrame(ur.boardNum, columns=['boardNum'])
        df['date'] = ur.date
        df['breakdown'] = ur.profitOrSpending
        df['category'] = ur.category
        df['price'] = ur.price
        df['etc'] = ur.etc

        df.to_csv("moneyBook.csv", index=False)

    # 데이터 삭제
    def deleteData(self, User, df):
        boardNum = int(input("삭제 할 거래번호 선택 : \n"))
        # Drop the row with the specified boardNum
        dfDeleted = df.drop(df[df['boardNum'] == boardNum].index)

        # Clear the user's lists
        User.boardNum.clear()
        User.date.clear()
        User.profitOrSpending.clear()
        User.category.clear()
        User.price.clear()
        User.etc.clear()

        # Iterate over the modified DataFrame to update the user's lists
        for row in dfDeleted.itertuples(index=False):
            User.boardNum.append(row[0])
            User.date.append(row[1])
            User.profitOrSpending.append(row[2])
            User.category.append(row[3])
            User.price.append(row[4])
            User.etc.append(row[5])

        df = pd.DataFrame(User.boardNum, columns=['boardNum'])
        df['date'] = User.date
        df['breakdown'] = User.profitOrSpending
        df['category'] = User.category
        df['price'] = User.price
        df['etc'] = User.etc

        df.to_csv("moneyBook.csv", index=False)


def main():
    ur = moneyBookData.User
    print("=============================== 데이터 취득 ==================================")
    cd = ControlData
    df = cd.readCsvData(self=ControlData ,file_path='moneyBook.csv', User=ur)
    print("============================================================================")
    selection = int(input("1. 데이터 저장 / 2. 데이터 불러오기 / 3. 데이터 수정 /4. 데이터 삭제 / 5. 종료\n"))
    # 데이터 저장
    if selection == 1:
        cd.createData(self=cd, User=ur)
        del ur

    # 데이터 불러오기
    elif selection == 2:
        cd.readAllData(self=cd, User=ur)
        del ur

    # 데이터 수정
    elif selection == 3:
        cd.modifyData(self=cd, ur=ur)
        del ur

    # 데이터 삭제
    elif selection == 4:
        cd.deleteData(self=cd, User=ur, df=df)
        del ur

    else:
        return 0

    main()

main()
