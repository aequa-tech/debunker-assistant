import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware



import yaml



basePath="/internal/v1/"

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

with open('explainability/APIfake_payload.yaml') as f:
    result = yaml.load(f, Loader=yaml.FullLoader)


@app.post(basePath+"hello")
async def hello(request_id : str, language: str = 'it'):
    return result['evaluation']

@app.post(basePath+"evaluation/{language}/{request_id}")
async def evaluation(request_id : str, language: str = 'it'):
    return result['evaluation']

@app.post(basePath+"explanation/{analysis_id}/{explanation_type}")
async def explanation(analysis_id : str, explanation_type : str):
    if explanation_type == 'affective':
        return result['explanation']['explanationAffective']
    elif explanation_type == 'dangerous':
        return result['explanation']['explanationDangerous']
    elif explanation_type == 'network':
        return result['explanation']['explanationNetwork']


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8090)