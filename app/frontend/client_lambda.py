import gradio as gr
import pandas as pd
import dotenv
import logging
import boto3
from botocore.exceptions import ClientError
import os
import json

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

### AWS Lambda funtion ### => AWS 람다 함수를 호출하는 함수
# S3 버킷에 데이터 생성
def lambda_addData(date,profitOrSpending,category,price,etc):
    lambda_client = boto3.client('lambda')
    lambda_client.invoke(FunctionName='moneyBook_CRUD_Handler',
                        InvocationType='RequestResponse',
                        Payload=json.dumps({
                            "CRUD": "create",
                            "date": date,
                            "profitOrSpending": profitOrSpending,
                            "category": category,
                            "price": price,
                            "etc": etc
                        })
                    )
    return True

# S3 버킷에 데이터 읽기
def lambda_readData():
    lambda_client = boto3.client('lambda')
    response = lambda_client.invoke(FunctionName='moneyBook_CRUD_Handler',
                        InvocationType='RequestResponse',
                        Payload=json.dumps({
                            "CRUD": "read",
                        })
                    )
    payloadedResponse = response['Payload'].read().decode('utf-8')
    responseToJson = json.loads(payloadedResponse)
    data = responseToJson
    df = pd.DataFrame(data)
    return df

# S3 버킷에 데이터 수정
def lambda_modifyData(boardNum,date,profitOrSpending,category,price,etc):
    lambda_client = boto3.client('lambda')
    lambda_client.invoke(FunctionName='moneyBook_CRUD_Handler',
                        InvocationType='RequestResponse',
                        Payload=json.dumps({
                            "CRUD": "modify",
                            "boardNum": boardNum,
                            "date": date,
                            "profitOrSpending": profitOrSpending,
                            "category": category,
                            "price": price,
                            "etc": etc
                        })
                    )
    return True

# S3 버킷에 데이터 삭제
def lambda_deleteData(boardNum,date,profitOrSpending,category,price,etc):
    lambda_client = boto3.client('lambda')
    lambda_client.invoke(FunctionName='moneyBook_CRUD_Handler',
                        InvocationType='RequestResponse',
                        Payload=json.dumps({
                            "CRUD": "delete",
                            "boardNum": boardNum,
                            "date": date,
                            "profitOrSpending": profitOrSpending,
                            "category": category,
                            "price": price,
                            "etc": etc
                        })
                    )
    return True
# ================ AWS function ================
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
        fn=lambda_addData, 
        inputs=([inputDate, inputPos, inputCategory, inputPrice, inputEtc]), 
        outputs=None
        )

# GUI의 조회 버튼 액션
def readAction():
    view_interface = gr.Interface(
        fn = lambda_readData, inputs=None, 
        outputs="dataframe", 
        title="가계부", 
        allow_flagging='never'
        )

# GUI의 수정 버튼 액션
def modifyAction():
    selectBoardNum = gr.Number(label="수정 할 거래번호")
    inputDate = gr.Textbox(label="날짜",placeholder="YYYY-MM-DD")
    inputPos = gr.Radio(["수입", "지출"], label="분류")
    inputCategory = gr.Textbox(label="카테고리",placeholder="카테고리를 입력해주세요")
    inputPrice = gr.Number(label="금액")
    inputEtc = gr.Textbox(label="메모", placeholder="메모를 입력할 수 있습니다")
    correctionButton = gr.Button("수정")
    correctionButton.click(lambda_modifyData, 
                           inputs=([selectBoardNum,inputDate,inputPos,inputCategory,inputPrice,inputEtc]),
                           outputs=None)

## GUI의 삭제 버튼 액션
def deleteAction():
    selectBoardNum = gr.Number(label="삭제 할 거래번호")
    correctionButton = gr.Button("삭제")
    correctionButton.click(lambda_deleteData, 
                           inputs=([selectBoardNum]), 
                           outputs=None)
# ================ Gradio function ================

def interface():
    with gr.Blocks() as app_interface:
        with gr.Tab("조회"):
            view_interface = gr.Interface(
                fn=lambda_readData,
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