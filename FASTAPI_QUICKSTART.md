# 🚀 FastAPI Integration - Quick Reference

## ✅ **SETUP COMPLETE**

Your L1 Pricing Model is now available as a REST API!

---

## 📋 **Quick Start (3 Steps)**

### **Step 1: Install Dependencies**
```bash
pip install -r requirements.txt
```

### **Step 2: Start the API Server**
```bash
python start_api.py
```

### **Step 3: Access the API**
- **Swagger UI:** http://localhost:8000/docs
- **API Root:** http://localhost:8000

---

## 🎯 **Main Endpoint**

### **POST** `/api/v1/predict`

**Request:**
```json
{
  "product": "3 Part Automated Hematology Analyzer",
  "quantity": 5
}
```

**Response:**
```json
{
  "product": "3 Part Automated Hematology Analyzer",
  "quantity": 5,
  "low_price": 390000,
  "high_price": 410000,
  "price_type": "TOTAL_CONTRACT",
  "confidence": "85%",
  "basis": "filtered_company.csv (L1 percentile pricing)",
  "competitors_analyzed": 10,
  "timestamp": "2026-01-11T10:53:27.123456"
}
```

---

## 🔗 **All Available Endpoints**

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information |
| GET | `/health` | Health check |
| GET | `/api/v1/status` | System status |
| POST | `/api/v1/predict` | Get pricing prediction |

---

## 💻 **Usage Examples**

### **Python**
```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/predict",
    json={
        "product": "3 Part Automated Hematology Analyzer",
        "quantity": 5
    }
)
result = response.json()
print(f"Price Range: ₹{result['low_price']:,.2f} - ₹{result['high_price']:,.2f}")
```

### **cURL**
```bash
curl -X POST http://localhost:8000/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{"product": "3 Part Automated Hematology Analyzer", "quantity": 5}'
```

### **JavaScript**
```javascript
fetch('http://localhost:8000/api/v1/predict', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    product: "3 Part Automated Hematology Analyzer",
    quantity: 5
  })
})
.then(res => res.json())
.then(data => console.log(data));
```

---

## 🧪 **Testing**

### **Run Test Suite**
```bash
python test_api.py
```

### **Manual Test**
```bash
# Health check
curl http://localhost:8000/health

# Pricing prediction
curl -X POST http://localhost:8000/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{"product": "Fully Automatic Biochemistry Analyzer", "quantity": 10}'
```

---

## 📚 **Interactive Documentation**

Once the server is running, access:

- **Swagger UI (Try it out!):** http://localhost:8000/docs
- **ReDoc (Beautiful docs):** http://localhost:8000/redoc

---

## ⚙️ **Server Configuration**

### **Default**
```bash
python start_api.py
# Host: 0.0.0.0
# Port: 8000
# Auto-reload: Enabled
```

### **Custom**
```bash
# Change port
python start_api.py --port 5000

# Production mode (no reload)
python start_api.py --no-reload

# Localhost only
python start_api.py --host 127.0.0.1
```

---

## 🛠️ **Files Created**

| File | Purpose |
|------|---------|
| `api_main.py` | Main FastAPI application |
| `start_api.py` | Server startup script |
| `test_api.py` | API test suite |
| `API_DOCUMENTATION.md` | Comprehensive documentation |
| `requirements.txt` | Python dependencies |

---

## ⚠️ **Important Notes**

### **Before Running:**
1. ✅ Close all CSV files in Excel
2. ✅ Run `python check_file_locks.py` to verify
3. ✅ Ensure data files exist in `data/raw/`

### **L1 Pricing Features:**
- ✅ **Total Contract Prices** (not unit prices)
- ✅ **L1-Specific Learning** (bottom 5-10 percentile)
- ✅ **No Price Rescaling** (quantity factor = 1.0)
- ✅ **Minimum Price Guardrail** (₹50,000)
- ✅ **Confidence Scoring** (based on data points)

---

## 🚦 **Status Codes**

| Code | Meaning | Action |
|------|---------|--------|
| 200 | Success | Pricing returned |
| 404 | Not Found | No competitors for product |
| 422 | Validation Error | Check request format |
| 500 | Server Error | Check file locks / data files |
| 503 | Service Unavailable | Data files missing |

---

## 🔥 **Common Issues & Solutions**

### **Issue: Cannot connect to API**
```bash
# Solution: Start the server
python start_api.py
```

### **Issue: File is locked**
```bash
# Solution: Close Excel, then check
python check_file_locks.py
```

### **Issue: No competitors found**
```bash
# Solution: Check product name, try broader terms
# Example: "Hematology Analyzer" instead of full name
```

---

## 📊 **Response Fields Explained**

| Field | Description | Example |
|-------|-------------|---------|
| `low_price` | Aggressive L1 bid (2% undercut) | 390000 |
| `high_price` | Conservative L1 bid (0.5% undercut) | 410000 |
| `price_type` | Always "TOTAL_CONTRACT" | "TOTAL_CONTRACT" |
| `confidence` | Win probability % | "85%" |
| `competitors_analyzed` | Data points used | 10 |
| `basis` | Learning method | "L1 percentile pricing" |

---

## 🎯 **Next Steps**

1. **Start Server:**
   ```bash
   python start_api.py
   ```

2. **Open Browser:**
   - http://localhost:8000/docs

3. **Try Interactive API:**
   - Click "POST /api/v1/predict"
   - Click "Try it out"
   - Enter product and quantity
   - Click "Execute"

4. **Integrate with Your App:**
   - Use Python/JavaScript examples above
   - Replace localhost with your server URL

---

## 📞 **Support**

- **Documentation:** `API_DOCUMENTATION.md`
- **Test Suite:** `python test_api.py`
- **Health Check:** `curl http://localhost:8000/health`
- **Status:** `curl http://localhost:8000/api/v1/status`

---

## ✅ **Summary**

**You now have:**
- ✅ RESTful API for L1 pricing predictions
- ✅ Interactive Swagger UI documentation
- ✅ Automated test suite
- ✅ Production-ready error handling
- ✅ CORS support for frontend integration
- ✅ Comprehensive validation

**API is ready for:**
- 🌐 Web application integration
- 📱 Mobile app backend
- 🔗 Third-party integrations
- ☁️ Cloud deployment

---

**🚀 Start serving L1 pricing predictions via API!**

```bash
python start_api.py
```

Then visit: **http://localhost:8000/docs**
