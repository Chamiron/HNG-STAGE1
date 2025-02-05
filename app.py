from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (modify for security)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model for the response
class NumberClassification(BaseModel):
    number: int
    is_prime: bool
    is_perfect: bool
    properties: list[str]
    digit_sum: int
    fun_fact: str

# Function to check if a number is prime
def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(abs(n) ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

# Function to check if a number is perfect
def is_perfect(n: int) -> bool:
    if n < 1:
        return False
    return n == sum(i for i in range(1, n) if n % i == 0)

# Function to check if a number is an Armstrong number
def is_armstrong(n: int) -> bool:
    digits = [int(d) for d in str(abs(n))]
    power = len(digits)
    return sum(d ** power for d in digits) == abs(n)

# Function to fetch fun fact from Numbers API
def get_fun_fact(n: int) -> str:
    try:
        response = requests.get(f"http://numbersapi.com/{n}/math?json")
        if response.status_code == 200:
            return response.json().get("text", "No fact available.")
    except:
        return "No fact available."
    return "No fact available."

@app.get("/api/classify-number", response_model=NumberClassification)
def classify_number(number: str = Query(..., description="Input number to classify")):
    # Validate input
    try:
        # Attempt to convert to float first to handle floating-point numbers
        number = float(number)
        # Convert to integer if it's a whole number
        if number.is_integer():
            number = int(number)
        else:
            raise ValueError
    except ValueError:
        # Return 400 Bad Request for invalid inputs
        raise HTTPException(
            status_code=400,
            detail={"number": number, "error": True},
        )

    properties = []
    if is_armstrong(number):
        properties.append("armstrong")
    properties.append("odd" if number % 2 != 0 else "even")

    return {
        "number": number,
        "is_prime": is_prime(number),
        "is_perfect": is_perfect(number),
        "properties": properties,
        "digit_sum": sum(map(int, str(abs(number)))),
        "fun_fact": get_fun_fact(number),
    }
