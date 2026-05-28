# 🎓 University Expense Prediction & Analytics System

An AI-powered full-stack web application that predicts university expenses using Machine Learning and provides real-time analytics dashboards with forecasting, authentication, and interactive visualizations.

---

# 🚀 Live Demo

## 🌐 Frontend

https://realtime-expense-prediction.vercel.app/

## ⚡ Backend API

https://university-expense-api.onrender.com/

---

# 📌 Project Overview

This project helps universities analyze and predict expenses using Machine Learning algorithms and real-time analytics.

The system provides:

- Expense Prediction
- Forecasting Future Expenses
- Department-wise Analysis
- Real-time Interactive Dashboard
- Admin Authentication
- Dataset Upload & Processing
- AI-powered Analytics

---

# 🧠 Machine Learning Workflow

## ✅ Data Preprocessing

The uploaded dataset undergoes:

- Duplicate Removal
- Missing Value Handling
- Date Conversion
- Outlier Handling using IQR
- Feature Engineering
- Data Scaling

---

## ✅ Feature Engineering

Additional features created:

- Expense_Per_Student
- Utility_Expenses
- Admission_Expenses
- Month
- Year
- Day

---

# 🤖 Machine Learning Models Used

## Base Models

- Linear Regression
- Decision Tree Regressor
- Support Vector Regressor (SVR)
- KNeighbors Regressor

## Meta Model

- Random Forest Regressor

## Final Ensemble Model

- Stacking Regressor

---

# ❓ Why Stacking Regressor?

University expense data contains:

- Linear Relationships
- Nonlinear Patterns
- Seasonal Trends
- Complex Feature Dependencies

Using a single model may not capture all patterns effectively.

### ✅ Stacking Advantages

- Combines multiple ML models
- Improves prediction accuracy
- Reduces overfitting
- Better generalization
- More robust predictions

---

# 📊 Model Evaluation Metrics

The model evaluates:

- MAE (Mean Absolute Error)
- MSE (Mean Squared Error)
- RMSE
- R² Score
- Training Accuracy
- Testing Accuracy

---

# 🔐 Authentication System

The project includes JWT-based Admin Authentication.

## Admin Credentials

```text
Username: admin
Password: admin123
```

---

# 📈 Features

## 🎯 AI Features

- Expense Prediction
- Future Forecasting
- Real-time Analytics
- ML Model Accuracy Tracking

---

## ⚡ Backend Features

- FastAPI REST APIs
- JWT Authentication
- Dataset Upload API
- Analytics APIs
- Forecast APIs
- Model Metrics APIs

---

## 🎨 Frontend Features

- Modern Dashboard UI
- Glassmorphism Design
- Interactive Charts
- Responsive Layout
- Real-time Prediction Updates
- Secure Login System

---

# 🛠️ Tech Stack

## Frontend

- React.js
- Axios
- Recharts
- CSS3

## Backend

- FastAPI
- Python
- Pandas
- NumPy
- Prophet

## Machine Learning

- Scikit-Learn
- Stacking Regressor
- Random Forest
- SVR
- KNN
- Linear Regression

## Deployment

- Vercel (Frontend)
- Render (Backend)
- GitHub (Version Control)

---

# 📂 Project Structure

```text
Realtime-expense-prediction
│
├── backend
│   ├── main.py
│   ├── processing.py
│   ├── train_model.py
│   ├── requirements.txt
│   ├── model.pkl
│   ├── scaler.pkl
│
├── frontend
│   ├── src
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── main.jsx
│   │
│   ├── package.json
│   ├── vite.config.js
│
└── README.md
```

---

# ⚙️ Installation Guide

# 1️⃣ Clone Repository

```bash
git clone https://github.com/AKASHAKKI26/Realtime-expense-prediction.git
```

---

# 2️⃣ Backend Setup

## Navigate to Backend

```bash
cd backend
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run FastAPI Server

```bash
uvicorn main:app --reload
```

Backend runs on:

```text
http://127.0.0.1:8000
```

---

# 3️⃣ Frontend Setup

## Navigate to Frontend

```bash
cd frontend
```

## Install Dependencies

```bash
npm install
```

## Run React App

```bash
npm run dev
```

Frontend runs on:

```text
http://localhost:5173
```

---

# 🔗 API Endpoints

# 🔐 Authentication

## Login

```http
POST /login
```

---

# 📤 Dataset Upload

## Upload Dataset

```http
POST /upload-dataset
```

Supports:
- CSV
- Excel (.xlsx)

---

# 🎯 Prediction API

## Predict Expense

```http
POST /predict
```

---

# 📊 Analytics APIs

## Expense Trends

```http
GET /expense-trends
```

## Department Analysis

```http
GET /department-analysis
```

## Forecast

```http
GET /forecast
```

## Feature Importance

```http
GET /feature-importance
```

## Metrics

```http
GET /metrics
```

---

# 📉 Forecasting

The project uses Facebook Prophet for future expense forecasting.

Forecast Features:
- Monthly Forecasting
- Trend Analysis
- Future Expense Prediction

---

# 🎨 Dashboard Features

## KPI Cards

- Predicted Expense
- Accuracy
- RMSE
- Total Records

## Charts

- Line Charts
- Bar Charts
- Pie Charts
- Area Charts

---

# 🌍 Deployment

## Frontend Deployment

Platform: Vercel

## Backend Deployment

Platform: Render

---

# 🔥 Future Enhancements

- Database Integration
- Role-based Authentication
- PDF Report Generation
- Email Notifications
- Docker Deployment
- AWS/GCP Deployment
- Dark/Light Mode
- Real Feature Importance
- User Management System

---

# 📸 Screenshots

## Login Page

- JWT Authentication
- Modern Glassmorphism UI

## Dashboard

- Expense Prediction
- Forecast Charts
- Analytics Dashboard
- Interactive Visualizations

---

# 👥 Team Contribution

This project was successfully developed by a team of 4 members, where each member contributed to different stages of the project development lifecycle.

| Team Member | Contribution |
|---|---|
| Member 1 | Selected the problem statement and performed dataset collection |
| Member 2 | Performed data analysis, preprocessing, cleaning, outlier handling, and feature engineering pipeline |
| Member 3 | Developed and trained the complete Machine Learning model and handled ML concepts, model evaluation, and forecasting |
| Member 4 | Developed FastAPI backend APIs, authentication system, frontend dashboard UI, deployment, and integration |

---

# 🤝 Team Collaboration

The project was developed collaboratively using:

- Machine Learning
- Full Stack Development
- Data Engineering
- API Development
- Authentication Systems
- Dashboard Design
- Cloud Deployment

Each member contributed to building a complete end-to-end AI-powered analytics platform.

---
---

# ⭐ If You Like This Project

Give this repository a ⭐ on GitHub.
