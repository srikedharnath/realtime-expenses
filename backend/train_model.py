import pandas as pd
import numpy as np
from processing import process

# Copy of the final_df for prediction
def train_model(final_df):
    prediction_df = final_df.copy()

    # Converting Categorical data to Numerical
    prediction_df=pd.get_dummies(
        prediction_df,columns=['Department'])

    # Splitting X and y data
    X = prediction_df.drop(columns='Total_Expenses')
    y = prediction_df['Total_Expenses']

    # Scaling the data
    from sklearn.preprocessing import StandardScaler
    scaler=StandardScaler()
    scaled_x=scaler.fit_transform(X)

    from sklearn.model_selection import train_test_split
    X_train,X_test,y_train,y_test = train_test_split(scaled_x,y,random_state=42,test_size=0.2)

    # Training the data using STACKING Algorithm
    from sklearn.linear_model import LinearRegression
    from sklearn.tree import DecisionTreeRegressor
    from sklearn.svm import SVR
    from sklearn.neighbors import KNeighborsRegressor

    # Importing the Base models
    base_models = [
        ('lr',LinearRegression()),
        ('dt',DecisionTreeRegressor()),
        ('svr',SVR()),
        ('knn',KNeighborsRegressor())
    ]

    # Importing meta model
    from sklearn.ensemble import RandomForestRegressor
    meta_model=RandomForestRegressor()

    # Training data using STACKING Regressor
    from sklearn.ensemble import StackingRegressor

    stack_model = StackingRegressor(estimators=base_models,final_estimator=meta_model)

    stack_model.fit(X_train,y_train)

    # Predicting the model
    y_pred = stack_model.predict(X_test)

    # Evaluation metrics of model
    from sklearn.metrics import (mean_absolute_error,mean_squared_error,r2_score)

    # Mean Absolute Error
    mae = mean_absolute_error(y_test,y_pred)
    # Mean Squared Error
    mse = mean_squared_error(y_test,y_pred)
    # Root mean squared error
    rmse = np.sqrt(mse)
    # r2 Score
    score = r2_score(y_test,y_pred)

    print("\nMAE :", mae)
    print("MSE :", mse)
    print("RMSE :", rmse)
    print("R2 Score :", score)

    return {

    "model": stack_model,

    "mae": mae,

    "mse": mse,

    "rmse": rmse,

    "r2_score": score,

    "accuracy": score * 100
}


