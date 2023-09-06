#서버 실행할때 쓰는 코드 terminal에 복붙 uvicorn main:app --reload
#UI로 자동 작성된 페이지 http://127.0.0.1:8000/docs

from fastapi import FastAPI, Query
from pydantic import BaseModel
from gpt_prompt import gpt_input_values #gpt로 결과 출력
from dalle import use_dalle #달리로 url출력

app = FastAPI()
app.state.prompt_dalle = "" #달리에 넣을값 미리 지정

#입력 받을 형태
# {
#   "product": "가방",
#   "basic_info": "35세/여/변호사/화려함",
#   "detail_info": "색상은 화려한 걸 좋아하지만 전반적으로 안정적이고 깔끔한 것을 좋아함"
# }
class Item(BaseModel):
    product: str
    basic_info: str
    detail_info: str | None = None

#자료 내보내기
@app.post("/gpt/")
def create_item(item: Item):
    print(item) #잘 들어왔는지 확인
    product = item.product
    basic_info = item.basic_info
    detail_info = item.detail_info

    #2개, 3개인지에 따라 다르게 값이 들어감
    if detail_info is None:
        input_values = (product, basic_info)
    else:
        input_values = (product, basic_info, detail_info)

    result = gpt_input_values(input_values)

    #if/else로 응답 형태 파악하기 result["제품디자인"]결과가 list인지 아닌지->프롬프트 고쳤더니 json형태 오류나서 if/else로 풀어냄
    if isinstance(result["제품디자인"], list):
        app.state.prompt_dalle = product + ', ' + ', '.join(result["제품디자인"]) + ', product full shot'
    else:
        app.state.prompt_dalle = product + ', ' + result["제품디자인"] + ', product full shot'
    #달리에 보낼때 이런식으로 손 써줘야함
    return result

@app.post("/using_dalle/")
def using_dalle(): #함수랑 같은 제목 쓰면 안됨!
    prompt_dalle = app.state.prompt_dalle #위에서 나온 결과로 이미지 생성하기
    print(f'prompt_dalle:{prompt_dalle}')
    img_url = use_dalle(prompt_dalle)

    return img_url

