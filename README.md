🔶 TRON-CHECKER
---
---

## 🔹 Quick-Start:

#### Install requirements:

```bash
pip install -r requirements.txt
```

#### Init migrations:

```bash
alembic upgrade eaac49fb3a17
```

#### Run uvicorn-server:

```bash
python src/main.py
```

---

## 🔹 Usage:

### ⚠️ Necessarily ⚠️:

> **Set your tron data provider API-KEY in .env.test**
> 
> **Example: # .env.test: BASE_TRON_KEY=QWERTY12356...**
> 
> **It is generally recommended to use TronGrid**
> 
> **But you can also use another provider or multiple providers by slightly changing the implementation**

#### Defined routes (URLs):

This service provides "clean" APIs for receiving and writing data about TRON Wallets

```
1. Get-info (With pagination) -> http://127.0.0.1:8000/api/records/get/?page=<PAGE_POSITIVE_NUMBER>
# Page -> dynamic parameter

2. Add-info-in-DB ->  http://127.0.0.1:8000/api/records/add/?address=<ADDRESS>
# Only for curl, postman - testing
```

---

#### Docs:

Intuitively understandable

```
URL: http://127.0.0.1:8000/docs
```

---

## 🔹 Additional tools:

#### Flake8:

```shell
flake8 ./
```

#### Mypy:

```shell
mypy ./
```

#### Tests:

```shell
pytest -v
```