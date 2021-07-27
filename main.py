import requests
import time
import csv

# 결과값 테이블의 헤더입니다.
# 주석과 바로 밑에 있는 데이터가 1:1 관계로 이어져 있습니다.
#         mainNo patientNo patientArea firstDate remarks
header = ["번호", "환자번호", "지역", "확진일자", "비고"]


# 현재 코로나 확진자에 대한 정보를 표시합니다.
# @param pageNum [number] : 불러올 페이지 번호
def get_info(pageNum):
    response = requests.post("https://www.incheon.go.kr/fnct/corona/mainSumTab1.json", {
        'curPage': pageNum
    })

    if response.status_code != 200:
        print("request failed : " + str(response.status_code))

    data = response.json()["list"]

    print(str(data["curPage"]) + "번째 데이터를 가져오는 중...")

    return data


def formatInfo(info):
    result = []

    for r in info:
        # 만약 patientNo가 0이라면 patientNoH로 값을 결정합니다.
        if r["patientNo"] == 0:
            r["patientNo"] = r["patientNoH"]

        # result array에 값을 추가합니다.
        result.append([
            r["mainNo"],
            r["patientNo"],
            r["patientArea"],
            r["firstDate"],
            r["remarks"],
        ])

    return result


# 결과를 담을 array
resultArray = [header]

# 최초 테이블 정보를 불러옵니다.
firstRow = get_info(1)
resultArray.extend(formatInfo(firstRow["listObject"]))

# 전체 페이지의 값
totalPage = firstRow["totalPage"]

# 2부터 totalPage + 1 까지 순회하며 0.5초 간격으로 데이터를 불러옵니다.
for i in range(2, totalPage + 1):
    row = get_info(i)
    resultArray.extend(formatInfo(row["listObject"]))
    time.sleep(0.5)

# csv file writer init
file = open("./dist/info.csv", "w", newline="")
writer = csv.writer(file)

# resultArray에 있는 값을 csv 파일에 덮어씌웁니다.
for row in resultArray:
    writer.writerow(row)

# 파일 쓰기를 종료합니다.
file.close()
