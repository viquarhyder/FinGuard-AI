# 🛡️ FinGuard AI

### AI-Powered Financial Fraud Detection \& Transaction Risk Assessment

FinGuard AI is an end-to-end financial security system that combines
machine learning fraud classification, anomaly detection, intelligent
risk scoring, and SHAP-based explainable AI in a Flask web application.

## 🚀 Highlights

* 🔍 Machine-learning based fraud detection
* 🧠 Isolation Forest anomaly detection
* ⚖️ Unified 0--100 transaction risk scoring
* 📊 Model comparison and optimization
* 🧠 SHAP explainable AI
* 🌐 Flask web dashboard
* 💳 Transaction-level risk assessment
* 💾 Git LFS support for large CSV datasets and reports

## 🧩 System Workflow

``` text
Raw Data → EDA → Preprocessing → Feature Engineering
                    ↓
              Model Training
              ↙           ↘
     Fraud Classification   Anomaly Detection
              ↘           ↙
               Risk Engine
                    ↓
             Explainable AI
                    ↓
             Flask Dashboard
```

## 🤖 Machine Learning

The training workflow includes:

Model                  Role

\---

Logistic Regression    Baseline classifier
Random Forest          Ensemble classifier
XGBoost                Gradient-boosted classifier
HistGradientBoosting   Gradient boosting
Isolation Forest       Anomaly detection

## ⚠️ Risk Engine

The risk engine combines:

* Fraud score: **70%**
* Anomaly score: **30%**

Risk bands:

&#x20;       Score Level

\---

&#x20;    0--39.99 🟢 Low
    40--69.99 🟡 Medium
      70--100 🔴 High


## 🧠 Explainable AI

The project uses SHAP to provide:

* Global feature importance
* Individual transaction explanations
* Feature contribution analysis

## 📊 Dataset

The project uses the standard credit-card fraud dataset with:

* 284,807 transactions
* 492 fraudulent transactions
* `Time`
* `V1`--`V28`
* `Amount`
* `Class`

Feature engineering adds transaction, behavioral, amount, time, and
risk-related features. The final engineered model input contains 53
features.

Risk-related features include:

* `Risk\_Deviation\_Score`
* `Risk\_Max\_Deviation`
* `Risk\_Extreme\_Ratio`
* `Risk\_Severe\_Ratio`

## 📁 Project Structure

``` text
FinGuard AI/
├── api/
├── config/
├── Dataset/
├── Models/
├── Notebooks/
├── Reports/
├── screenshots/
├── src/
├── static/
├── templates/
├── Tests/
├── app.py
├── requirements.txt
├── .gitignore
├── .gitattributes
└── LICENSE
```

## 📓 Notebook Pipeline

1. `01\_Data\_Loading.ipynb`
2. `02\_Exploratory\_Data\_Analysis.ipynb`
3. `03\_Data\_Preprocessing.ipynb`
4. `04\_Feature\_Engineering.ipynb`
5. `05\_Model\_Training.ipynb`
6. `06\_Model\_Comparison\_Optimization.ipynb`
7. `07\_Final\_Model\_Prediction.ipynb`
8. `08\_Anomaly\_Detection.ipynb`
9. `09\_Risk\_Engine.ipynb`
10. `10\_Explainable\_AI.ipynb`

## 🌐 Flask Application

The web application provides:

* Home
* Security Dashboard
* Transaction Analysis
* Prediction
* Analytics
* User Analysis
* About
* Health Check

The prediction interface can present risk score, risk level, fraud
probability, anomaly status, transaction amount, recommended decision,
and engine/model status.

## 🛠️ Technology Stack

**Languages \& Frameworks:** Python, Flask, HTML, CSS, JavaScript

**ML \& Data:** Scikit-learn, XGBoost, SHAP, NumPy, Pandas, Matplotlib,
Seaborn

**Model Persistence:** Joblib, Pickle

**Version Control:** Git, GitHub, Git LFS

## ⚙️ Installation

``` bash
git clone https://github.com/viquarhyder/FinGuard-AI.git
cd FinGuard-AI

conda create -n finguard python=3.10
conda activate finguard

pip install -r requirements.txt
git lfs install
git lfs pull
```

## ▶️ Run

``` bash
python app.py
```

Open the local Flask URL shown by the application.

## 📦 Git LFS

Large datasets and generated CSV reports are managed with Git LFS. Git
LFS should be installed before pulling the complete project data.

## 🔐 Security

Do not commit API keys, passwords, tokens, or private credentials. Keep
secrets outside the repository and review `.gitignore` before adding
local configuration files.

## 🔮 Future Improvements

* Real-time transaction streaming
* Behavioral user profiling
* Model drift monitoring
* Automated fraud alerts
* Cloud deployment
* Authentication and role-based access
* Production database integration

## 📄 License

This project is licensed under the **MIT License**. See
[`LICENSE`](LICENSE).

## 👨‍💻 Author

**Mohammed Viquar Hyder**

GitHub: [@viquarhyder](https://github.com/viquarhyder)

\---

### 🛡️ FinGuard AI

**Detect Fraud. Assess Risk. Protect Every Transaction.**

