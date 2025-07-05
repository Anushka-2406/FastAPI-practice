from fastapi import FastAPI
import json
app = FastAPI()

def load_data():
    with open('data.json', 'r') as file:
        return json.load(file)



@app.get('/')
def read():
    return {'message': 'Hello, World!'}
@app.get("/data")
def data():
    data = load_data()
    return {"data": data}