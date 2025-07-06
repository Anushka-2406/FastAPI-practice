from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Optional, List, Dict, Annotated, Literal
import json


# Creating a pydantic model for the data structure
class Patient(BaseModel):
    id: Annotated[str,Field(..., description='ID of the patient')]

    name : Annotated[str, Field(..., description='Name of the patient')]
    city : Annotated[str, Field(..., description='City of the patient')]
    age: Annotated[int, Field(..., gt=0,lt=120, description='Age of the patient')]
    gender : Annotated[Literal['Male','Female','Other'], Field(..., description='Gender of the patient')]
    height: Annotated[float, Field(..., gt=0, description='Height of the patient in cm')]
    weight: Annotated[float, Field(..., gt=0, description='Weight of the patient in kg')]
    
    @computed_field
    @property
    def bmi(self)-> float:
        """Calculate the Body Mass Index (BMI) of the patient."""
        return round(self.weight / (self.height ** 2), 2)
    
    @computed_field
    @property
    def verdict(self) ->str:
        if(self.bmi <18.5):
            return 'Underweight'
        elif(self.bmi >= 18.5 and self.bmi < 24.9):
            return 'Normal weight'
        elif(self.bmi >= 25 and self.bmi < 29.9):
            return 'Overweight'
        else:
            return 'Obesity'
    









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
def get_patient(patient_id: str = Path(..., description='ID of patient',examples='P001')):
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
def patient_info(patient_info: str=Path(..., description='ID of patient', examples='P001')):
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

@app.post('/create')
def create_patient(patient: Patient):
    data = load_data()
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient with this ID already exists")
    
    data[patient.id] = patient.model_dump(exclude={'id'})
    
    with open('data.json', 'w') as file:
        json.dump(data, file)
    
    return JSONResponse(status_code=201, content={"message": "Patient created successfully"})