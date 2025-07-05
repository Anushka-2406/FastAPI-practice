from fastapi import FastAPI, Path, HTTPException, Query
import json
app = FastAPI()

def load_data():
    with open('data.json', 'r') as file:
        return json.load(file)

"""This is a simple FastAPI application that reads data from a JSON file."""

@app.get('/')
def read():
    return {'message': 'Hello, World!'}


@app.get("/data")
def data():
    data = load_data()
    return {"data": data}

"""Understandinhg path params : 
   - Path parameters are dynamic segments of the URL that can change.
   - They are defined in the route using curly braces {}.
   - They allow you to capture values from the URL and use them in your function.
   - Example: /items/{item_id} captures the item_id from the URL.
"""

@app.get('/patients/{patient_id}')
def get_patient(patient_id: str = Path(..., description='ID of patient',example='P001')):
    data =load_data()
    if patient_id in data: 
        return data[patient_id]
    else : 
        return {"error": "Patient not found"}
    
    # We use Path in order to enchance the readability of parameters and to add validation.
    # We can add Title, description, example, regex, min_length, max_length, ge(greater than or equal to),gt,le,lt etc.
    # we add this in input side

    """To handle http errors, we can use the HTTPException class from fastapi.exceptions.
    - It allows us to raise an exception with a specific status code and detail message.
    - Example: raise HTTPException(status_code=404, detail="Item not found")
    """
@app.get('/patient_info/{patient_info}')
def patient_info(patient_info: str=Path(..., description='ID of patient', example='P001')):
    data=load_data()

    if patient_info in data:
        return data[patient_info]
    else:
        raise HTTPException(status_code=404,detail='Patient not found')
    
    """To handle query parameters, we can use the Query class from fastapi.
    - It allows us to define optional parameters in the URL.
    - Example: /items?name=example captures the name query parameter.
    - We can also add validation, default values, and descriptions to query parameters.
    - It also allows us to sort the data based on the query parameters.
    """

@app.get('/sortf')
def sort_f(sort_by : str =Query(..., description='sort by field'),order : str = Query('asc')):

        valid_fields =['height','weight','bmi']

        if sort_by not in valid_fields:
            raise HTTPException(status_code=400,detail=f'Pick from valid fields only {valid_fields}')
        
        if order not in ['asc','desc']:
            raise HTTPException(status_code=400,detail=f'Order must be either asc or desc')
        
        data1=load_data()

        data_new=sorted(data1.values(),key=lambda x : x.get(sort_by,0),reverse=True if order=='desc' else False)
        return {'data': data_new}