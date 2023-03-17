# Install FastAPI framework
# pip3 install "fastapi[all]"
# https://fastapi.tiangolo.com/tutorial/

# uvicorn main:app --reload
# python -m uvicorn main:app --reload
import uvicorn
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.staticfiles import StaticFiles
from typing import Union

from demohouse import build_demo_house
from device import Device
from sensors import *
from actuators import *

# in fastAPI we can send json or python dictonary(dict will automaticly be converted to json)

app = FastAPI()

smart_house = build_demo_house()

# http://localhost:8000/welcome/index.html
app.mount("/welcome", StaticFiles(directory="static"), name="static")


# http://localhost:8000/
@app.get("/")
async def root():
    return {"message": "Welcome to SmartHouse Cloud REST API - Powered by FastAPI"}


@app.get("/smarthouse")
async def smarthouse():
    """information on the smart house"""
    return smart_house


@app.get("/smarthouse/floor")
async def smarthouse():
    """ information on all floors"""
    return smart_house.floors


@app.get("/smarthouse/floor/{fid}")
async def smarthouse(fid: int):
    """information about a floor given by fid"""
    try:
        return smart_house.floors[fid]
    except IndexError:
        raise HTTPException(status_code=404, detail="Index out of range")


# feil i oppgaven?
@app.get("/smarthouse/floor/{fid}/room/")
async def smarthouse(fid: int):
    """information about all rooms on a given floor fid"""
    try:
        return smart_house.floors[fid].rooms
    except IndexError:
        raise HTTPException(status_code=404, detail="Index out of range")


@app.get("/smarthouse/floor/{fid}/room/{rid}")
async def smarthouse(fid: int, rid: int):
    """information about a specific room rid on a given floor fid"""
    try:
        return smart_house.floors[fid].rooms[rid]
    except IndexError:
        raise HTTPException(status_code=404, detail="Index out of range")


@app.get("/smarthouse/device")
async def device():
    """information on all devices"""
    return smart_house.get_all_devices()

@app.get("/smarthouse/device/{did}")
async def device(did: int):
    """information for a given device did"""
    try:
        return smart_house.get_all_devices()[did]
    except KeyError:
        raise HTTPException(status_code=404, detail="No such device id")


@app.get("/smarthouse/sensor/{did}/current")
async def sensor(did: int):
    """get current sensor measurement for sensor did"""
    try:
        return smart_house.get_all_devices()[did].get_current_value
    except KeyError:
        raise HTTPException(status_code=404, detail="No such device id")
    except AttributeError:
        raise HTTPException(status_code=400, detail="Device requested is not a sensor")


'''


'''
@app.post("/smarthouse/sensor/{did}/current", status_code=201)
async def sensor(did: int, measurement: SensorMeasurement):
    """add measurement for sensor did
    POST BODY
    {
    "value": "9"
    }
    """
    try:
        smart_house.get_all_devices()[did].set_current_value(float(measurement.value))
        return "Measurement value {0} added to device {1}".format(measurement.value, did)
    except KeyError:
        raise HTTPException(status_code=404, detail="No such device id")

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
    #house = build_demo_house()
    #did = 14
    #a = smart_house.get_all_devices()[did]
    #a.set_current_value(2.5)
    #b = smart_house.get_all_devices()[did]
    #c = 1
