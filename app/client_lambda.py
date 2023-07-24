import gradio as gr
import pandas as pd
import dotenv
import logging
import boto3
from botocore.exceptions import ClientError
import os
import json

boardNum = []
date = []
profitOrSpending = []
category = []
price = []
etc = []

# ================ AWS function ================
dotenv.load_dotenv(".env", override=True)
# S3 버킷에 데이터 업로드
def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

# S3 버킷에 데이터 생성
def create_new_file(file_name):
    lambda_client = boto3.client('lambda')
    lambda_client.invoke(FunctionName='createCSVFile',
                        InvocationType='RequestResponse',
                        Payload=json.dumps({
                            "file_name": file_name
                        })
                    )
    
    return True
# ================ AWS function ================
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

# ================ CRUD function ================
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
    upload_file('app/moneyBook.csv', 'moneybook-bucket-cho', 'moneyBook.csv')

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
        upload_file('app/moneyBook.csv', 'moneybook-bucket-cho', 'moneyBook.csv')

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
        upload_file('app/moneyBook.csv', 'moneybook-bucket-cho', 'moneyBook.csv')
    else:
        print("입력하신 거래번호가 존재하지 않습니다.")
# ================ CRUD function ================

# ================ Gradio function ================
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

## GUI의 삭제 버튼 액션
def deleteAction():
    readCsvData()
    selectBoardNum = gr.Number(label="삭제 할 거래번호")
    correctionButton = gr.Button("삭제")
    correctionButton.click(deleteData, 
                           inputs=([selectBoardNum]), 
                           outputs=None)
# ================ Gradio function ================

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