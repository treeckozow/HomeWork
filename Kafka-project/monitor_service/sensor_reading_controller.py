from fastapi import APIRouter, Request

router = APIRouter()

async def calculate_average(data: dict, appliance_key: str) -> float:
    """Helper function to calculate average, returning 0 if count is 0."""
    sum_value = data["sum"].get(appliance_key, 0)
    count_value = data["count"].get(appliance_key, 0)
    return sum_value / count_value if count_value > 0 else 0

@router.get("/avg")
async def avg_get(request: Request):
    sensor_data = request.app.state.SENSOR_DATA
    averages = {}
    
    # Use a loop to populate power_data
    for appliance in sensor_data["sum"]:
        averages[appliance] = str(await calculate_average(sensor_data, appliance))
    
    return averages
