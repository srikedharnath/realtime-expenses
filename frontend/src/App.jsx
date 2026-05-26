import { useState } from "react";

import axios from "axios";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  Legend,
  AreaChart,
  Area
} from "recharts";

import "./App.css";

function App() {

  // =========================================
  // STATES
  // =========================================

  const [username, setUsername] =
useState("");

const [password, setPassword] =
useState("");

const [isLoggedIn,
setIsLoggedIn] =
useState(

  localStorage.getItem("token")
  ? true
  : false
);
  
  const [prediction, setPrediction] =
    useState({

      value: null,

      time: Date.now()
    });

  const [loading, setLoading] =
    useState(false);

  const [predictLoading,
    setPredictLoading] =
      useState(false);

  const [metrics, setMetrics] =
    useState(null);

  const [file, setFile] =
    useState(null);

  const [expenseTrendData,
    setExpenseTrendData] =
      useState([]);

  const [departmentData,
    setDepartmentData] =
      useState([]);

  const [featureImportanceData,
    setFeatureImportanceData] =
      useState([]);

  const [forecastData,
    setForecastData] =
      useState([]);

  // =========================================
  // COLORS
  // =========================================

  const COLORS = [

    "#3b82f6",

    "#8b5cf6",

    "#10b981",

    "#f59e0b",

    "#ef4444"
  ];

  const loginAdmin = async () => {

  try {

    const formData =
      new URLSearchParams();

    formData.append(
      "username",
      username
    );

    formData.append(
      "password",
      password
    );

    const response =
      await axios.post(

        "https://university-expense-api.onrender.com/login",

        formData,

        {
          headers: {

            "Content-Type":
            "application/x-www-form-urlencoded"
          }
        }
      );

    localStorage.setItem(

      "token",

      response.data.access_token
    );

    setIsLoggedIn(true);

    alert("Login Success");

  }

  catch (error) {

    alert("Invalid Credentials");
  }
};

  // =========================================
  // FORM DATA
  // =========================================

  const [formData, setFormData] =
    useState({

      Date: "01-06-2026",

      Student_Count: 1500,

      Faculty_Salary: 4000000,

      Non_Teaching_Salary: 1000000,

      Electricity_Bill: 500000,

      Internet_Charges: 40000,

      Water_Bill: 80000,

      Maintenance_Cost: 90000,

      Lab_Expenses: 70000,

      Library_Expenses: 45000,

      Software_License_Cost: 50000,

      Examination_Expenses: 30000,

      Workshop_Expenses: 25000,

      Placement_Training_Cost: 60000,

      Event_Expenses: 35000,

      Transport_Expenses: 120000,

      Cleaning_Security_Cost: 50000,

      Miscellaneous_Expenses: 25000,

      Department: "AI"
    });

  // =========================================
  // FETCH ANALYTICS
  // =========================================

  const fetchAnalytics = async () => {

    try {

      const [
        expenseResponse,
        departmentResponse,
        featureResponse,
        forecastResponse
      ] = await Promise.all([

        axios.get(
          "https://university-expense-api.onrender.com/expense-trends"
        ),

        axios.get(
          "https://university-expense-api.onrender.com/department-analysis"
        ),

        axios.get(
          "https://university-expense-api.onrender.com/feature-importance"
        ),

        axios.get(
          "https://university-expense-api.onrender.com/forecast"
        )
      ]);

      setExpenseTrendData(
        [...expenseResponse.data]
      );

      setDepartmentData(
        [...departmentResponse.data]
      );

      setFeatureImportanceData(
        [...featureResponse.data]
      );

      setForecastData(
        [...forecastResponse.data]
      );

    }

    catch (error) {

      console.log(error);
    }
  };

  // =========================================
  // HANDLE INPUT
  // =========================================

  const handleChange = (e) => {

    const { name, value } =
      e.target;

    setFormData((prev) => ({

      ...prev,

      [name]:

        name === "Department"

        ||

        name === "Date"

        ?

        value

        :

        Number(value)
    }));
  };

const logoutAdmin = () => {

  localStorage.removeItem(
    "token"
  );

  setIsLoggedIn(false);

  setMetrics(null);

  setPrediction({

    value:null,

    time:Date.now()
  });
};



if (!isLoggedIn) {

  return (

    <div className="login-page">

      <div className="login-overlay"></div>

      <div className="login-card">

        <div className="login-header">

          <div className="login-icon">

            🎓

          </div>

          <h1>
            University Expense AI
          </h1>

          <p>
            Admin Authentication Portal
          </p>

        </div>

        <div className="login-form">

          <div className="input-group">

            <label>
              Username
            </label>

            <input
              type="text"
              placeholder="Enter Admin Username"
              value={username}
              onChange={(e)=>
                setUsername(
                  e.target.value
                )
              }
            />

          </div>

          <div className="input-group">

            <label>
              Password
            </label>

            <input
              type="password"
              placeholder="Enter Password"
              value={password}
              onChange={(e)=>
                setPassword(
                  e.target.value
                )
              }
            />

          </div>

          <button
            className="login-btn"
            onClick={loginAdmin}
          >

            Login to Dashboard

          </button>

        </div>

        <div className="login-footer">

          Secure AI Powered
          University Analytics System

        </div>

      </div>

    </div>
  );
}
  // =========================================
  // UPLOAD DATASET
  // =========================================

  const uploadDataset = async () => {

    if (!file) {

      alert("Please select dataset");

      return;
    }

    const uploadFormData =
      new FormData();

    uploadFormData.append(
      "file",
      file
    );

    setLoading(true);

    // SAFE RESET

    setPrediction({

      value: null,

      time: Date.now()
    });

    setExpenseTrendData([]);

    setDepartmentData([]);

    setFeatureImportanceData([]);

    setForecastData([]);

    try {

      const response =
        await axios.post(
  "https://university-expense-api.onrender.com/upload-dataset",
  uploadFormData,
  {
    headers: {

      "Content-Type":
      "multipart/form-data",

      Authorization:
      `Bearer ${
        localStorage.getItem("token")
      }`
    }
  }
);

      setMetrics(
        response.data
      );

      await fetchAnalytics();

      alert(
        response.data.message
      );

    }

    catch (error) {

      console.log(error);

      alert(

        error.response?.data?.error ||

        "Upload Failed"
      );
    }

    finally {

      setLoading(false);
    }
  };

  // =========================================
  // PREDICT
  // =========================================

  const predictExpense = async () => {

  try {

    setPredictLoading(true);

    const response =
      await axios.post(

  "https://university-expense-api.onrender.com/predict",

  formData,

  {
    headers: {

      "Content-Type":
      "application/json",

      Authorization:
      `Bearer ${
        localStorage.getItem("token")
      }`
    }
  }
);

    console.log(
      "NEW PREDICTION:",
      response.data
    );

    const newValue =
      parseFloat(

        response.data
        .Predicted_Expense
      );

    // IMPORTANT

    setPrediction({

      value: newValue,

      time: Date.now()
    });

  }

  catch (error) {

    console.log(error);

    alert(
      "Prediction Failed"
    );
  }

  finally {

    setPredictLoading(false);
  }
};



  // =========================================
  // UI
  // =========================================

  return (
    

    <div className="dashboard">

      <div className="topbar">

  <h1>
    University Expense Analytics Dashboard
  </h1>

  <button
    className="logout-btn"
    onClick={logoutAdmin}
  >

    Logout

  </button>

</div>

      {/* KPI */}

      <div className="card-grid">

        {/* PREDICTION */}

        <div className="card">

  <h3>
    Predicted Expense
  </h3>

  <h2>

    {

      predictLoading

      ?

      "Calculating..."

      :

      prediction &&
      prediction.value !== null

      ?

      `₹${prediction.value.toLocaleString()}`

      :

      "₹0"
    }

  </h2>

</div>

        {/* ACCURACY */}

        <div className="card">

          <h3>
            Accuracy
          </h3>

          <h2>

            {

              metrics

              ?

              `${metrics.accuracy.toFixed(2)}%`

              :

              "0%"
            }

          </h2>

        </div>

        {/* RMSE */}

        <div className="card">

          <h3>
            RMSE
          </h3>

          <h2>

            {

              metrics

              ?

              metrics.rmse.toFixed(2)

              :

              "0"
            }

          </h2>

        </div>

        {/* TOTAL ROWS */}

        <div className="card">

          <h3>
            Total Records
          </h3>

          <h2>

            {

              metrics

              ?

              metrics.total_rows

              :

              "0"
            }

          </h2>

        </div>

      </div>

      {/* UPLOAD */}

      <div className="glass-card">

        <h2>
          Upload Dataset
        </h2>

        <input
          className="file-input"
          type="file"
          accept=".xlsx,.csv"
          onChange={(e)=>

            setFile(
              e.target.files[0]
            )
          }
        />

        <button
          className="predict-btn"
          onClick={uploadDataset}
        >

          {

            loading

            ?

            "Training Model..."

            :

            "Upload Dataset"
          }

        </button>

      </div>

      {/* FORM */}

      <div className="glass-card">

        <h2>
          Predict Expense
        </h2>

        <div className="form-grid">

          {

            Object.keys(formData)

            .map((key)=>(

              <div key={key}>

                <label>
                  {key}
                </label>

                {

                  key === "Department"

                  ?

                  <select
                    name={key}
                    value={formData[key]}
                    onChange={handleChange}
                  >

                    <option value="AI">
                      AI
                    </option>

                    <option value="DS">
                      DS
                    </option>

                    <option value="CS">
                      CS
                    </option>

                  </select>

                  :

                  <input
                    type={
                      key === "Date"
                      ?
                      "text"
                      :
                      "number"
                    }
                    name={key}
                    value={formData[key]}
                    onChange={handleChange}
                  />
                }

              </div>

            ))
          }

        </div>

        <button
          className="predict-btn"
          onClick={predictExpense}
        >

          {

            predictLoading

            ?

            "Predicting..."

            :

            "Predict Expense"
          }

        </button>

      </div>

      {/* CHARTS */}

      {

        metrics && (

          <div className="charts-grid">

            {/* LINE */}

            <div className="chart-card">

              <h2>
                Monthly Expense Trend
              </h2>

              <ResponsiveContainer
                width="100%"
                height={350}
              >

                <LineChart
                  data={expenseTrendData}
                >

                  <CartesianGrid
                    strokeDasharray="3 3"
                  />

                  <XAxis
                    dataKey="Month"
                  />

                  <YAxis />

                  <Tooltip />

                  <Line
                    type="monotone"
                    dataKey="Total_Expenses"
                    stroke="#3b82f6"
                    strokeWidth={4}
                  />

                </LineChart>

              </ResponsiveContainer>

            </div>

            {/* BAR */}

            <div className="chart-card">

              <h2>
                Department Analysis
              </h2>

              <ResponsiveContainer
                width="100%"
                height={350}
              >

                <BarChart
                  data={departmentData}
                >

                  <CartesianGrid
                    strokeDasharray="3 3"
                  />

                  <XAxis
                    dataKey="Department"
                  />

                  <YAxis />

                  <Tooltip />

                  <Bar
                    dataKey="Total_Expenses"
                    fill="#8b5cf6"
                  />

                </BarChart>

              </ResponsiveContainer>

            </div>

            {/* PIE */}

            <div className="chart-card">

              <h2>
                Expense Distribution
              </h2>

              <ResponsiveContainer
                width="100%"
                height={350}
              >

                <PieChart>

                  <Pie
                    data={featureImportanceData}
                    dataKey="importance"
                    nameKey="feature"
                    outerRadius={120}
                    label
                  >

                    {

                      featureImportanceData.map(

                        (entry,index)=>(

                          <Cell
                            key={index}
                            fill={
                              COLORS[
                                index %
                                COLORS.length
                              ]
                            }
                          />

                        )
                      )
                    }

                  </Pie>

                  <Tooltip />

                  <Legend />

                </PieChart>

              </ResponsiveContainer>

            </div>

            {/* FORECAST */}

            <div className="chart-card">

              <h2>
                Future Forecast
              </h2>

              <ResponsiveContainer
                width="100%"
                height={350}
              >

                <AreaChart
                  data={forecastData}
                >

                  <CartesianGrid
                    strokeDasharray="3 3"
                  />

                  <XAxis
                    dataKey="Date"
                  />

                  <YAxis />

                  <Tooltip />

                  <Area
                    type="monotone"
                    dataKey="Predicted_Expense"
                    stroke="#10b981"
                    fill="#10b981"
                  />

                </AreaChart>

              </ResponsiveContainer>

            </div>

          </div>
        )
      }

    </div>
  );
}

export default App;