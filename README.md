# 🚨 Explainable AI–Based Fraud Detection System for Public Sector Spending

An end-to-end, explainable fraud detection system designed to analyze public sector procurement and spending data, identify anomalous transactions, and provide transparent, auditor-friendly explanations using machine learning.

This project focuses on **real-world applicability**, **explainability**, and **auditability**, making it suitable for government, public sector, and compliance-driven environments.

---

## 📌 Project Motivation

Fraud, waste, and abuse in public spending are difficult to detect due to:
- Large volumes of financial data
- Complex and evolving spending patterns
- Limited transparency in automated systems

This project addresses these challenges by combining:
- **Machine Learning–based anomaly detection**
- **Explainable AI (XAI)**
- **Secure APIs with full audit logging**

---

## ⚙️ How the System Works

1. **Data Ingestion**
   - Supports real-world public datasets (CSV files from local or remote sources)
   - Example: UK government spending datasets

2. **Feature Engineering**
   - Derives transactional and contextual features
   - Captures temporal and behavioral patterns

3. **Fraud Detection (ML)**
   - Uses **Isolation Forest** to learn normal spending behavior
   - Flags transactions that significantly deviate from learned patterns

4. **Explainable AI**
   - Uses **SHAP** to explain why a transaction was flagged
   - Explanations are converted into auditor-friendly insights

5. **Security & Auditability**
   - Role-based authentication (Admin / Auditor)
   - Every sensitive action is logged for traceability

6. **Results & Review**
   - Suspicious transactions can be reviewed via secure APIs
   - Explanations help auditors make informed decisions

---

## 🧰 Tech Stack

- **Backend:** Python, FastAPI  
- **Database:** PostgreSQL  
- **Machine Learning:** Scikit-learn (Isolation Forest)  
- **Explainability:** SHAP  
- **Security:** JWT Authentication, Role-Based Access Control  
- **Audit:** Action-level audit logging  
- **Deployment:** Cloud-ready, environment-based configuration  

---

## 🚀 Current Features

- ✔ Anomaly-based fraud detection  
- ✔ Explainable AI for transparency  
- ✔ Real-world dataset ingestion  
- ✔ Secure APIs with authentication  
- ✔ Comprehensive audit logging  
- ✔ Production-ready architecture  

---

## 🛣️ Roadmap – Planned Advanced Features (Prioritized)

This project is **actively evolving**. Planned enhancements include:

1. **Vendor Network & Graph Analysis**
   - Detect collusion patterns using graph-based relationships

2. **Unstructured Data Processing (OCR + NLP)**
   - Extract insights from invoices and contracts (PDFs)

3. **Model Monitoring & Drift Detection**
   - Detect changes in data behavior and trigger retraining

4. **Real-Time / Streaming Analysis**
   - Support near real-time transaction ingestion

5. **Auditor Case Management Workflow**
   - Assign, review, and resolve fraud cases

6. **Advanced Explainability**
   - Contrastive and natural-language explanations

---

## 📊 Demo Data

The system can be tested using:
- Public government spending datasets
- Any compatible financial dataset after basic preprocessing

---

## 🤝 Open Source & Contributions

This is an **open-source project**, and contributions are welcome 🎉

- Fork the repository
- Create a feature branch
- Submit a pull request

Suggestions, issues, and feature requests are highly encouraged.

---

## 📄 License

This project is released under the **MIT License**.

---

## 🙌 Acknowledgements

Built as a learning-focused and production-minded project to explore:
- AI/ML automation
- Explainable AI
- Fraud detection in public sector systems
