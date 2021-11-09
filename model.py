from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel


class Car(BaseModel):
    name: str
    brand: str
    price: str
    color_name: dict
    color_code: dict
    fuel_type: str
    vehicle_type: str
    engine_displacement: str
    power: str
    torque: str
    seating_capacity: str
    door: str
    length: str
    width: str
    height: str
    ground_clearance: str
    wheel_base: str
    curb_weight: str
    fuel_tank_capacity: str
    cylinders: str
    valves_per_cylinder: str
    compression_ratio: str
    valve_configuration: str
    engine: str
    front_suspension: str
    rear_suspension: str
    transmission_type: str
    transmission: str
    tyre_size: str
    wheel_size: str
    alloy_wheel_size: str
    tyre_type: str
    steering_gear_type: str
    adjustable_steering_wheel: str
    steering_wheel_adjustment_type: str

    def to_json(self):
        return jsonable_encoder(self, exclude_none=True)


class Prediction(BaseModel):
    prediction: str
    accuracy: float

    def to_bson(self):
        data = self.dict(by_alias=True, exclude_none=True)
        if data.get("_id") is None:
            data.pop("_id", None)
        return data
