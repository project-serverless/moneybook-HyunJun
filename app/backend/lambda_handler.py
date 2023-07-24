import pandas as pd
import json
import boto3
import io

boardNum = []
date = []
profitOrSpending = []
category = []
price = []
etc = []  

def lambda_handler(event, context):
    # S3 버킷과 파일 이름 설정
    bucket_name = 'moneybook-bucket-cho'
    file_name = 'moneyBook.csv'
    
    # S3 클라이언트 생성
    s3_client = boto3.client('s3')
    
    # S3 객체 가져오기
    response = s3_client.get_object(Bucket=bucket_name, Key=file_name)

    # CSV 파일을 데이터프레임으로 읽기
    df = pd.read_csv(response['Body'])
    
    # 데이터 프레임을 배열에 저장
    for row in df.itertuples(index=False):
        boardNum.append(row[0])
        date.append(row[1])
        profitOrSpending.append(row[2])
        category.append(row[3])
        price.append(row[4])
        etc.append(row[5])
        
    # newDf = {
    #     "boardNum": df['boardNum'],
    #     "date": df['date'],
    #     "profitOrSpending": df['profitOrSpending'],
    #     "category": df['category'],
    #     "price": df['price'],
    #     "etc": df['etc']
    # }
    # json_data = json.loads(newDf)
    
    crud = event["CRUD"]
    if(crud == "create"):
        data = createData(df=df, event=event)
        s3_client.put_object(Bucket=bucket_name, Key=file_name, Body=data)
    elif(crud == "read"):
        print(readCSV(df))
        return readCSV(df)
    elif(crud == "modify"):
        data = modifyData(df=df, event=event)
        s3_client.put_object(Bucket=bucket_name, Key=file_name, Body=data)
    elif(crud == "delete"):
        data = deleteData(df=df, event=event)
        s3_client.put_object(Bucket=bucket_name, Key=file_name, Body=data)
    
    return {
        'statusCode': 200,
        'body': "Success"
    }
    
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
def createData(df, event):
    initData()
    for row in df.itertuples(index=False):
        boardNum.append(row[0])
        date.append(row[1])
        profitOrSpending.append(row[2])
        category.append(row[3])
        price.append(row[4])
        etc.append(row[5])
    if(len(boardNum) == 0):
        boardNum.append(1)
    else:
        boardNum.append(boardNum[-1]+1)
    date.append(event['date'])
    profitOrSpending.append(event['profitOrSpending'])
    category.append(event['category'])
    price.append(event['price'])
    etc.append(event['etc'])
    
    df = pd.DataFrame(boardNum, columns=['boardNum'])
    df['date'] = date
    df['profitOrSpending'] = profitOrSpending
    df['category'] = category
    df['price'] = price
    df['etc'] = etc
    data = df.to_csv().encode()
    return data
    
def readCSV(df):
    newDf = {
        "boardNum": df['boardNum'].tolist(),
        "date": df['date'].tolist(),
        "profitOrSpending": df['profitOrSpending'].tolist(),
        "category": df['category'].tolist(),
        "price": df['price'].tolist(),
        "etc": df['etc'].tolist()
    }
    json_data = json.dumps(newDf).encode('utf-8')
    return json_data

# 데이터 수정(Update)
def modifyData(df, event):
    initData()
    for row in df.itertuples(index=False):
        boardNum.append(row[0])
        date.append(row[1])
        profitOrSpending.append(row[2])
        category.append(row[3])
        price.append(row[4])
        etc.append(row[5])
    if event['boardNum'] in boardNum:
        date[boardNum.index(event['boardNum'])] = event['date']
        profitOrSpending[boardNum.index(event['boardNum'])] = event['profitOrSpending']
        category[boardNum.index(event['boardNum'])] = event['category']
        price[boardNum.index(event['boardNum'])] = event['price']
        etc[boardNum.index(event['boardNum'])] = event['etc']

        newDf = pd.DataFrame(boardNum, columns=['boardNum'])
        df['date'] = date
        df['profitOrSpending'] = profitOrSpending
        df['category'] = category
        df['price'] = price
        df['etc'] = etc
        data = df.to_csv().encode()
        return data

    else:
        print("입력하신 거래번호가 존재하지 않습니다.")

# 데이터 삭제(Delete)
def deleteData(df, event):
    initData()
    dfDeleted = df.drop(df[df['boardNum'] == event['boardNum']].index)
    if event['boardNum'] in boardNum:
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
        df['profitOrSpending'] = profitOrSpending
        df['category'] = category
        df['price'] = price
        df['etc'] = etc
        data = dfDeleted.to_csv().encode()
        return data
    else:
        print("입력하신 거래번호가 존재하지 않습니다.")
# ================ CRUD function ================