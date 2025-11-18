
# 🩺 Diabetes Risk Prediction – Machine Learning Application using Docker

A fully-containerized Machine Learning application that trains a diabetes prediction model and serves real-time predictions through a FastAPI backend and a modern, responsive HTML UI.
This project demonstrates **modular MLOps architecture**, **containerization**, and **reproducible ML workflows** using Docker.

---

## 🚀 Project Overview

This project predicts whether a patient is at **risk of diabetes** using medical features such as glucose levels, blood pressure, BMI, insulin levels, and more.

It consists of **two coordinated Docker containers**:

### **1️⃣ Training Container (ML Pipeline)**

* Loads the diabetes dataset
* Cleans and preprocesses data using a Scikit-Learn pipeline
* Trains a Logistic Regression model
* Saves:

  * `model.pkl` (trained ML model)
  * `preprocess.pkl` (preprocessing pipeline)

These are stored in the shared `model/` directory.

### **2️⃣ API Container (FastAPI Backend + UI)**

* Loads the trained model + preprocessor
* Hosts a **REST API (`/predict`)** to evaluate patient data
* Serves a **beautiful UI** at `http://localhost:8000`

Users simply input medical values → API returns:

✔ **Low Diabetes Risk**
⚠ **High Diabetes Risk**

---

## 🧱 Architecture

```
diabetes_docker_project/
│── api/
│   ├── app.py              # FastAPI app
│   ├── ui/
│   │   └── index.html      # Frontend interface
│   └── Dockerfile.api
│
│── training/
│   ├── preprocess.py       # Preprocessing pipeline
│   ├── train.py            # Model training code
│   └── Dockerfile.train
│
│── data/
│   └── diabetes.csv        # Dataset (Pima Indians Diabetes Dataset)
│
│── model/                  # Auto-generated model + preprocessor
│── docker-compose.yml      # Orchestrates multi-container setup
```

---

## 🐳 How Docker Is Used

This project uses **Docker to isolate ML training and prediction**, ensuring reproducible results across any machine.

### **✔ Multi-container architecture**

* The **training container** handles *only* data prep + model training.
* The **API container** handles *only* serving predictions.

### **✔ Shared volume**

Both containers share:

```
./model:/app/model
```

This allows:

* training container → writes model
* API container → reads model
* without manual copying.

### **✔ Clean, reproducible environment**

No Python environment setup is needed — Docker ensures:

* Same Python version
* Same library versions
* Same behavior on any machine

Just run → get the same results every time.

---

## 🚀 How to Run the Project

### **1️⃣ Install Docker Desktop**

[https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/)

### **2️⃣ Open terminal in the project folder**

```
cd diabetes_docker_project
```

### **3️⃣ Build all containers**

```
docker-compose build --no-cache
```

### **4️⃣ Start the full system**

```
docker-compose up
```

### **5️⃣ Open the UI**

Navigate to:

👉 **[http://localhost:8000](http://localhost:8000)**

Enter patient values → get a prediction popup.
<img width="1420" height="1485" alt="image" src="https://github.com/user-attachments/assets/f2a14fb6-4431-44b4-adc4-c5eecfc231be" />
<img width="1470" height="952" alt="image" src="https://github.com/user-attachments/assets/2896cbe7-f454-41b7-a1fc-8757ac4340b8" />
<img width="2463" height="1592" alt="image" src="https://github.com/user-attachments/assets/263c6cc6-32ae-46e2-8f14-57f6b7630fe1" />
<img width="1379" height="1464" alt="image" src="https://github.com/user-attachments/assets/c2fd2517-eb5a-457d-9759-a3cfa62433f6" />




---

## 🧠 Machine Learning Details

### **Model Used**

**Logistic Regression**, due to:

* Stability
* Speed
* Good performance on structured medical datasets

### **Features**

* Pregnancies
* Glucose
* Blood Pressure
* Skin Thickness
* Insulin
* BMI
* Diabetes Pedigree Function
* Age

### **Preprocessing Pipeline**

Built with Scikit-Learn:

* Imputation (mean fill missing values)
* Standard scaling (StandardScaler)
* Consistent transformations for training & inference

---

## 🖥 Frontend UI

A polished HTML interface with:

* Individual input fields
* Ideal value hints
* A modern submit button
* A **pop-up alert box** showing risk level (High / Low)

No React or heavy frameworks — just clean HTML/CSS/JS served by FastAPI.

---

## 🔧 Endpoints

### **POST /predict**

Input:

```json
{
  "Pregnancies": 2,
  "Glucose": 145,
  "BloodPressure": 72,
  "SkinThickness": 20,
  "Insulin": 85,
  "BMI": 33.1,
  "DiabetesPedigreeFunction": 0.47,
  "Age": 50
}
```

Output:

```json
{
  "prediction": 1
}
```

Where:

* `0` → Low diabetes risk
* `1` → High diabetes risk

---

## 🛑 Stop Containers

```
CTRL + C
docker-compose down
```


