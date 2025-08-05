
## 1. Clone the Repository

git clone https://github.com/Harsh-Agarwals/demand_forecasting

cd demand_forecasting

## 2. Set Up Python Environment

python -m venv venv

venv\Scripts\activate (windows)

source venv/bin/activate (macOS, Linux)

## 3. Install Required Libraries

pip install -r requirements.txt

## Running the code

python final.py

[In case of changing filepath or model, just update the parameters in final.py]


### Assumption

- Dates formatted as YYYY-MM-DD

- holiday_dates column uses ;-separated strings or blank for no holidays

- 1 load_unit = 1 person required

- we are forecasting for next 7 days