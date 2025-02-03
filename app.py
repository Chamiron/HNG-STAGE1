from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

# Enable CORS (Allows API to be accessed from different domains)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (modify for security)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Function to check if a number is prime
def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

# Function to check if a number is perfect
def is_perfect(n: int) -> bool:
    return n == sum(i for i in range(1, n) if n % i == 0)

# Function to check if a number is an Armstrong number
def is_armstrong(n: int) -> bool:
    digits = [int(d) for d in str(n)]
    power = len(digits)
    return sum(d ** power for d in digits) == n

# Function to fetch fun fact from Numbers API
def get_fun_fact(n: int) -> str:
    try:
        response = requests.get(f"http://numbersapi.com/{n}/math?json")
        if response.status_code == 200:
            return response.json().get("text", "No fact available.")
    except:
        return "No fact available."
    return "No fact available."

@app.get("/api/classify-number")
def classify_number(number: int = Query(..., description="Input number to classify")):
    properties = []
    if is_armstrong(number):
        properties.append("armstrong")
    properties.append("odd" if number % 2 != 0 else "even")

    return {
        "number": number,
        "is_prime": is_prime(number),
        "is_perfect": is_perfect(number),
        "properties": properties,
        "digit_sum": sum(map(int, str(number))),
        "fun_fact": get_fun_fact(number)
    }
