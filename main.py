from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n):
    return n == sum(i for i in range(1, n) if n % i == 0)

def digit_sum(n):
    return sum(int(digit) for digit in str(n))

def is_armstrong(n):
    return n == sum(int(digit) ** len(str(n)) for digit in str(n))

@app.get("/number")
def get_number_properties(number: int):
    try:
        number = int(number)
    except ValueError:
        raise HTTPException(status_code=400, detail={"number": str(number), "error": True})

    properties = []
    if is_armstrong(number):
        properties.append("armstrong")
    properties.append("odd" if number % 2 != 0 else "even")

    fun_fact_response = requests.get(f'http://numbersapi.com/{number}/math')
    fun_fact = fun_fact_response.text if fun_fact_response.status_code == 200 else "No fun fact available."

    response = {
        "number": number,
        "is_prime": is_prime(number),
        "is_perfect": is_perfect(number),
        "properties": properties,
        "digit_sum": digit_sum(number),
        "fun_fact": fun_fact
    }

    return response

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

