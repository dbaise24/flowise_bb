import io
from openai import OpenAI
from dotenv import load_dotenv
import os
import httpx
import json

app = FastAPI(
    title="Flowise_parse_test",
    description=description,
    summary="test",
    version="1.0.0",
 
load_dotenv()
 
def build_url(workflow_name, version, init):
    url=f"https://artemis-arrow.bubbleapps.io/{version}/api/1.1/wf/{workflow_name}"
    if version=='live':
         url=f"https://artemis-arrow.bubbleapps.io/api/1.1/wf/{workflow_name}"
    if init==True:
        url=url+'/initialize'
    return url
 
async def run_chat(chatflow_id,data):
        async with httpx.AsyncClient(timeout=120) as client:
                chat_url=f"https://carry-schismless-ewa.ngrok-free.dev/api/v1/prediction/{chatflow_id}"
                resp = await client.post(chat_url, headers={"Authorization":f"Bearer {os.environ['flowise_key']}"},data=data)
                print(resp.raise_for_status())
                print(resp.content)
                output = resp.content.decode("utf-8")
                output=output.replace("b'{",'{').replace("}'","}")
                print("output= ", output)
 
                return json.loads(output)
@app.post("/post_dynamic_chat")
async def call_transcription(chatflow_id, x_input,obj_id,workflow_name,version,init=False,api_key:APIKeyHeader = Depends(auth.get_api_key)):
    data= await run_chat(chatflow_id=chatflow_id, data=x_input)
    callback_data={"data": data, "obj_id":obj_id}
    print("ddata ", callback_data)
    init=bool(init)
    print(init)
    url=build_url(workflow_name=workflow_name, version=version, init=init)
    print("url - ", url)
    async with httpx.AsyncClient() as client:
            resp = await client.post(url, headers={"Authorization":f"Bearer {os.environ['bubble_auth']}"},data=callback_data)
            print(f"Status: {resp.status_code}")
            print(f"Response: {resp.text}")
            print(f"Headers: {resp.headers}")
