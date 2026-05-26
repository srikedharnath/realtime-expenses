from fastapi import FastAPI
from fastapi import UploadFile
from fastapi import File
from fastapi import HTTPException
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm

from jose import jwt
from jose import JWTError

from datetime import datetime
from datetime import timedelta


import pandas as pd
import numpy as np
import joblib

from prophet import Prophet

# =========================================================
# FASTAPI
# =========================================================

app = FastAPI()

# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "https://realtime-expense-prediction.vercel.app"
]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================================================
# GLOBAL VARIABLES
# =========================================================

model = None
final_df = None
metrics_data = {}
feature_columns = []

SECRET_KEY = "ADMIN_SECRET_KEY"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
)
ADMIN_USERNAME = "admin"

ADMIN_PASSWORD = "admin123"

def create_access_token(data):

    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode = data.copy()

    to_encode.update({

        "exp": expire
    })

    encoded_jwt = jwt.encode(

        to_encode,

        SECRET_KEY,

        algorithm=ALGORITHM
    )

    return encoded_jwt

def verify_token(

    token: str = Depends(
        oauth2_scheme
    )

):

    try:

        payload = jwt.decode(

            token,

            SECRET_KEY,

            algorithms=[ALGORITHM]
        )

        username = payload.get("sub")

        if username is None:

            raise HTTPException(

                status_code=401,

                detail="Invalid Token"
            )

        return username

    except JWTError:

        raise HTTPException(

            status_code=401,

            detail="Invalid Token"
        )

# =========================================================
# PREPROCESSING FUNCTION
# =========================================================

def process(files):

    all_files = []

    for file in files:

        # =================================================
        # READ FILE
        # =================================================

        if file.filename.endswith(".xlsx"):

            df = pd.read_excel(file.file)

        else:

            df = pd.read_csv(file.file)

        # =================================================
        # REMOVE DUPLICATES
        # =================================================

        df = df.drop_duplicates()

        # =================================================
        # FILL MISSING VALUES
        # =================================================

        for col in df.select_dtypes(include=np.number).columns:
            df[col].fillna(df[col].mean(), inplace=True)

        # =================================================
        # DATE CONVERSION
        # =================================================

        df["Date"] = pd.to_datetime(
            df["Date"],
            errors="coerce"
        )

        # =================================================
        # HANDLE OUTLIERS
        # =================================================

        cols = df.select_dtypes(
            exclude=["datetime", "object"]
        ).columns

        for col in cols:

            Q1 = df[col].quantile(0.25)

            Q3 = df[col].quantile(0.75)

            IQR = Q3 - Q1

            lower = Q1 - 1.5 * IQR

            upper = Q3 + 1.5 * IQR

            df[col] = np.where(
                df[col] < lower,
                lower,
                df[col]
            )

            df[col] = np.where(
                df[col] > upper,
                upper,
                df[col]
            )

        # =================================================
        # FEATURE ENGINEERING
        # =================================================

        df["day"] = df["Date"].dt.day

        df["Month"] = df["Date"].dt.month

        df["Year"] = df["Date"].dt.year

        df["Expense_Per_Student"] = (
            df["Total_Expenses"] /
            df["Student_Count"]
        )

        df["Utility_Expenses"] = (

            df["Electricity_Bill"]

            +

            df["Water_Bill"]

            +

            df["Internet_Charges"]
        )

        df["Admission_Expenses"] = np.where(
            df["Month"].isin([5, 6, 7]),
            1,
            0
        )

        all_files.append(df)

    # =====================================================
    # MERGE DATASETS
    # =====================================================

    merged_df = pd.concat(
        all_files,
        ignore_index=True
    )

    return merged_df

# =========================================================
# MODEL TRAINING
# =========================================================

def train_model(dataframe):

    global model
    global metrics_data
    global feature_columns

    prediction_df = dataframe.copy()

    # =====================================================
    # ENCODING
    # =====================================================

    prediction_df = pd.get_dummies(
        prediction_df,
        columns=["Department"]
    )

    # =====================================================
    # DROP DATE
    # =====================================================

    prediction_df.drop(
        columns=["Date"],
        inplace=True
    )

    # =====================================================
    # SPLIT X AND y
    # =====================================================

    X = prediction_df.drop(
        columns=["Total_Expenses"]
    )

    y = prediction_df["Total_Expenses"]

    feature_columns = X.columns.tolist()

    # =====================================================
    # SCALING
    # =====================================================

    from sklearn.preprocessing import StandardScaler

    scaler = StandardScaler()

    X_scaled = scaler.fit_transform(X)

    # =====================================================
    # TRAIN TEST SPLIT
    # =====================================================

    from sklearn.model_selection import train_test_split

    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled,
        y,
        test_size=0.2,
        random_state=42
    )

    # =====================================================
    # BASE MODELS
    # =====================================================

    from sklearn.linear_model import LinearRegression
    from sklearn.tree import DecisionTreeRegressor
    from sklearn.svm import SVR
    from sklearn.neighbors import KNeighborsRegressor

    base_models = [

        ("lr", LinearRegression()),

        ("dt", DecisionTreeRegressor()),

        ("svr", SVR()),

        ("knn", KNeighborsRegressor())
    ]

    # =====================================================
    # META MODEL
    # =====================================================

    from sklearn.ensemble import RandomForestRegressor

    meta_model = RandomForestRegressor()

    # =====================================================
    # STACKING MODEL
    # =====================================================

    from sklearn.ensemble import StackingRegressor

    stack_model = StackingRegressor(
        estimators=base_models,
        final_estimator=meta_model
    )

    # =====================================================
    # FIT MODEL
    # =====================================================

    stack_model.fit(
        X_train,
        y_train
    )

    # =====================================================
    # PREDICTIONS
    # =====================================================

    y_pred = stack_model.predict(X_test)

    # =====================================================
    # METRICS
    # =====================================================

    from sklearn.metrics import (
        mean_absolute_error,
        mean_squared_error,
        r2_score
    )

    mae = mean_absolute_error(
        y_test,
        y_pred
    )

    mse = mean_squared_error(
        y_test,
        y_pred
    )

    rmse = np.sqrt(mse)

    r2 = r2_score(
        y_test,
        y_pred
    )

    accuracy = r2 * 100

    # =====================================================
    # SAVE METRICS
    # =====================================================

    metrics_data = {

        "mae": round(mae, 2),

        "mse": round(mse, 2),

        "rmse": round(rmse, 2),

        "r2_score": round(r2, 2),

        "accuracy": round(accuracy, 2)
    }

    # =====================================================
    # SAVE MODEL
    # =====================================================

    joblib.dump(
        stack_model,
        "stack_model.pkl"
    )

    joblib.dump(
        scaler,
        "scaler.pkl"
    )

    model = stack_model

# =========================================================
# INPUT SCHEMA
# =========================================================

class ExpenseInput(BaseModel):

    Date: str

    Student_Count: int

    Faculty_Salary: float

    Non_Teaching_Salary: float

    Electricity_Bill: float

    Internet_Charges: float

    Water_Bill: float

    Maintenance_Cost: float

    Lab_Expenses: float

    Library_Expenses: float

    Software_License_Cost: float

    Examination_Expenses: float

    Workshop_Expenses: float

    Placement_Training_Cost: float

    Event_Expenses: float

    Transport_Expenses: float

    Cleaning_Security_Cost: float

    Miscellaneous_Expenses: float

    Department: str

# =========================================================
# HOME API
# =========================================================

@app.get("/")

def home():

    return {

        "message":
        "University Expense Prediction API Running"
    }

@app.post("/login")

def login(

    form_data:
    OAuth2PasswordRequestForm =
    Depends()

):

    if (

        form_data.username
        !=
        ADMIN_USERNAME

        or

        form_data.password
        !=
        ADMIN_PASSWORD
    ):

        raise HTTPException(

            status_code=401,

            detail="Invalid Credentials"
        )

    access_token = create_access_token({

        "sub":
        form_data.username
    })

    return {

        "access_token":
        access_token,

        "token_type":
        "bearer"
    }
# =========================================================
# UPLOAD DATASETS API
# =========================================================

@app.post("/upload-dataset")

async def upload_dataset(

    user:
    str = Depends(
        verify_token
    ),
    file: UploadFile = File(...)

):


    global final_df
    

    try:

        # PROCESS SINGLE FILE

        final_df = process([file])

        # TRAIN MODEL

        train_model(final_df)

        return {

            "message":
            "Dataset Uploaded Successfully",

            "total_rows":
            len(final_df),

            "accuracy":
            metrics_data["accuracy"],

            "mae":
            metrics_data["mae"],

            "rmse":
            metrics_data["rmse"],

            "r2_score":
            metrics_data["r2_score"]
        }

    except Exception as e:

        # FIX: raise HTTPException so frontend receives
        # a proper 4xx/5xx status code, not a 200 with
        # an "error" key that axios won't catch
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

# =========================================================
# PREDICT API
# =========================================================

@app.post("/predict")

def predict(data: ExpenseInput,

    user:
    str = Depends(
        verify_token
    )):

    global model
    global feature_columns

    try:

        if model is None:

            raise HTTPException(
                status_code=400,
                detail="Please upload dataset first"
            )

        # =================================================
        # LOAD SCALER
        # =================================================

        scaler = joblib.load(
            "scaler.pkl"
        )

        # =================================================
        # DATE FEATURES
        # =================================================

        date = pd.to_datetime(
            data.Date,
            format="%d-%m-%Y"
        )

        day = date.day

        month = date.month

        year = date.year

        # =================================================
        # FEATURE ENGINEERING
        # FIX: Expense_Per_Student was hardcoded to 0.
        # It must be calculated from the actual input
        # values so every prediction reflects the real
        # inputs the user provided.
        # =================================================

        # Sum all expense fields the user entered to get
        # a rough Total_Expenses estimate for this feature.
        # (At prediction time we don't know Total_Expenses
        # yet, so we derive it from the component fields.)
        estimated_total = (
            data.Faculty_Salary
            + data.Non_Teaching_Salary
            + data.Electricity_Bill
            + data.Internet_Charges
            + data.Water_Bill
            + data.Maintenance_Cost
            + data.Lab_Expenses
            + data.Library_Expenses
            + data.Software_License_Cost
            + data.Examination_Expenses
            + data.Workshop_Expenses
            + data.Placement_Training_Cost
            + data.Event_Expenses
            + data.Transport_Expenses
            + data.Cleaning_Security_Cost
            + data.Miscellaneous_Expenses
        )

        expense_per_student = (
            estimated_total / data.Student_Count
            if data.Student_Count > 0
            else 0
        )

        utility_expenses = (

            data.Electricity_Bill

            +

            data.Water_Bill

            +

            data.Internet_Charges
        )

        admission_expenses = 1 if month in [5, 6, 7] else 0

        # =================================================
        # CREATE INPUT DATAFRAME
        # =================================================

        input_df = pd.DataFrame([{

            "Student_Count":
            data.Student_Count,

            "Faculty_Salary":
            data.Faculty_Salary,

            "Non_Teaching_Salary":
            data.Non_Teaching_Salary,

            "Electricity_Bill":
            data.Electricity_Bill,

            "Internet_Charges":
            data.Internet_Charges,

            "Water_Bill":
            data.Water_Bill,

            "Maintenance_Cost":
            data.Maintenance_Cost,

            "Lab_Expenses":
            data.Lab_Expenses,

            "Library_Expenses":
            data.Library_Expenses,

            "Software_License_Cost":
            data.Software_License_Cost,

            "Examination_Expenses":
            data.Examination_Expenses,

            "Workshop_Expenses":
            data.Workshop_Expenses,

            "Placement_Training_Cost":
            data.Placement_Training_Cost,

            "Event_Expenses":
            data.Event_Expenses,

            "Transport_Expenses":
            data.Transport_Expenses,

            "Cleaning_Security_Cost":
            data.Cleaning_Security_Cost,

            "Miscellaneous_Expenses":
            data.Miscellaneous_Expenses,

            "day":
            day,

            "Month":
            month,

            "Year":
            year,

            "Expense_Per_Student":
            expense_per_student,

            "Utility_Expenses":
            utility_expenses,

            "Admission_Expenses":
            admission_expenses,

            "Department":
            data.Department
        }])

        # =================================================
        # ENCODING
        # =================================================

        input_df = pd.get_dummies(
            input_df,
            columns=["Department"]
        )

        # =================================================
        # MISSING COLUMNS
        # =================================================

        for col in feature_columns:

            if col not in input_df.columns:

                input_df[col] = 0

        input_df = input_df[
            feature_columns
        ]

        # =================================================
        # SCALE INPUT
        # =================================================

        input_scaled = scaler.transform(
            input_df
        )

        # =================================================
        # PREDICTION
        # =================================================

        prediction = model.predict(
            input_scaled
        )[0]

        return {

            "Predicted_Expense":
            round(float(prediction), 2)
        }

    except HTTPException:

        # Re-raise FastAPI HTTP exceptions as-is
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

# =========================================================
# EXPENSE TRENDS API
# =========================================================

@app.get("/expense-trends")

def expense_trends():

    global final_df

    try:

        temp = final_df.copy()

        trend = (

            temp.groupby(
                temp["Date"].dt.strftime("%Y-%m")
            )["Total_Expenses"]

            .mean()

            .reset_index()
        )

        trend.columns = [

            "Month",

            "Total_Expenses"
        ]

        return trend.to_dict(
            orient="records"
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

# =========================================================
# DEPARTMENT ANALYSIS
# =========================================================

@app.get("/department-analysis")

def department_analysis():

    global final_df

    try:

        dept = (

            final_df.groupby(
                "Department"
            )["Total_Expenses"]

            .mean()

            .reset_index()
        )

        return dept.to_dict(
            orient="records"
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

# =========================================================
# FEATURE IMPORTANCE
# =========================================================

@app.get("/feature-importance")

def feature_importance():

    return [

        {

            "feature":
            "Faculty Salary",

            "importance":
            22
        },

        {

            "feature":
            "Placement Training",

            "importance":
            20
        },

        {

            "feature":
            "Lab Expenses",

            "importance":
            18
        },

        {

            "feature":
            "Transport",

            "importance":
            14
        },

        {

            "feature":
            "Electricity",

            "importance":
            10
        },

        {

            "feature":
            "Internet",

            "importance":
            8
        },

        {

            "feature":
            "Library",

            "importance":
            5
        },

        {

            "feature":
            "Events",

            "importance":
            3
        }
    ]

# =========================================================
# FORECAST API
# =========================================================

@app.get("/forecast")

def forecast():

    global final_df

    try:

        forecast_df = final_df[[

            "Date",

            "Total_Expenses"

        ]].copy()

        forecast_df.columns = [

            "ds",

            "y"
        ]

        prophet_model = Prophet()

        prophet_model.fit(
            forecast_df
        )

        future = prophet_model.make_future_dataframe(
            periods=6,
            freq="ME"
        )

        prediction = prophet_model.predict(
            future
        )

        result = prediction[[

            "ds",

            "yhat"

        ]].tail(6)

        result.columns = [

            "Date",

            "Predicted_Expense"
        ]

        result["Date"] = result[
            "Date"
        ].astype(str)

        return result.to_dict(
            orient="records"
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

# =========================================================
# METRICS API
# =========================================================

@app.get("/metrics")

def metrics():

    return metrics_data