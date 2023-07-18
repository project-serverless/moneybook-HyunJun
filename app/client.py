import gradio as gr
import pandas as pd

boardNum = []
date = []
profitOrSpending = []
category = []
price = []
etc = []

file_path="app/moneyBook.csv"

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
def createData(inputDate, inputPos, inputCategory, inputPrice : int, inputEtc):
    initData()
    readCsvData()
    if(len(boardNum) == 0):
        boardNum.append(boardNum+1)
    else:
        boardNum.append(boardNum[-1]+1)
    date.append(inputDate)
    profitOrSpending.append(inputPos)
    category.append(inputCategory)
    price.append(inputPrice)
    etc.append(inputEtc)
    
    df = pd.DataFrame(boardNum, columns=['boardNum'])
    df['date'] = date
    df['breakdown'] = profitOrSpending
    df['category'] = category
    df['price'] = price
    df['etc'] = etc
    df.to_csv("app/moneyBook.csv", index=False)
    initData()

# 데이터 불러오기(Read)
def readCsvData():
    initData()
    df = pd.read_csv("app/moneyBook.csv")
    for row in df.itertuples(index=False):
        boardNum.append(row[0])
        date.append(row[1])
        profitOrSpending.append(row[2])
        category.append(row[3])
        price.append(row[4])
        etc.append(row[5])
    return df

# 데이터 수정(Update)
def modifyData(selectBoardNum,inputDate,inputPos,inputCategory,inputPrice,inputEtc):
    initData()
    readCsvData()
    if selectBoardNum in boardNum:
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
def deleteData(selectBoardNum):
    initData()
    df = readCsvData()
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
        dfDeleted.to_csv("app/moneyBook.csv", index=False)
    else:
        print("입력하신 거래번호가 존재하지 않습니다.")

# GUI의 입력 버튼 액션
def createAction():
    inputDate = gr.Textbox(label="날짜", placeholder="YYYY-MM-DD")
    inputPos = gr.Radio(["수입", "지출"], label="분류")
    inputCategory = gr.Textbox(label="카테고리", placeholder="카테고리를 입력해주세요")
    inputPrice = gr.Number(label="금액")
    inputEtc = gr.Textbox(label="메모", placeholder="메모를 입력할 수 있습니다")
    input_button = gr.Button("입력하기")
    input_button.click(
        fn=createData, 
        inputs=([inputDate, inputPos, inputCategory, inputPrice, inputEtc]), 
        outputs=None
        )

# GUI의 조회 버튼 액션
def readAction():
    view_interface = gr.Interface(
        fn = readCsvData, inputs=None, 
        outputs="dataframe", 
        title="가계부", 
        allow_flagging='never'
        )

# GUI의 수정 버튼 액션
def modifyAction():
    readCsvData()
    selectBoardNum = gr.Number(label="수정 할 거래번호")
    inputDate = gr.Textbox(label="날짜",placeholder="YYYY-MM-DD")
    inputPos = gr.Radio(["수입", "지출"], label="분류")
    inputCategory = gr.Textbox(label="카테고리",placeholder="카테고리를 입력해주세요")
    inputPrice = gr.Number(label="금액")
    inputEtc = gr.Textbox(label="메모", placeholder="메모를 입력할 수 있습니다")
    correctionButton = gr.Button("수정")
    correctionButton.click(modifyData, 
                           inputs=([selectBoardNum,inputDate,inputPos,inputCategory,inputPrice,inputEtc]),
                           outputs=None)
    # index_interface = gr.Interface(fn = checkIndex, inputs=None, outputs="dataframe", title="가계부", allow_flagging='never')

## GUI의 삭제 버튼 액션
def deleteAction():
    readCsvData()
    selectBoardNum = gr.Number(label="삭제 할 거래번호")
    correctionButton = gr.Button("삭제")
    correctionButton.click(deleteData, 
                           inputs=([selectBoardNum]), 
                           outputs=None)
    # gr.Interface(fn=deleteData, inputs=([file_path, selectBoardNum]), outputs="dataframe", allow_flagging='never')

def interface():
    with gr.Blocks() as app_interface:
        with gr.Tab("조회"):
            view_interface = gr.Interface(
                fn=readCsvData,
                inputs=None, 
                outputs="dataframe",
                title="가계부",
                allow_flagging='never'
            )
        with gr.Tab("입력"):
            createAction()
            readAction() 
        with gr.Tab("수정"):
            readAction() 
            modifyAction()
        with gr.Tab("삭제"):
            readAction() 
            deleteAction()

    app_interface.launch()

if __name__ == "__main__":
    interface()