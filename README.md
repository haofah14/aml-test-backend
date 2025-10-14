## 1. clone repo

```
git clone https://github.com/haofah14/aml-test-backend
cd aml-test-backend
```

## 2. create venv

```
python -m venv venv
```

on windows:

```
venv\Scripts\activate
```

on macOS/linux:

```
source venv/bin/activate
```

## 3. install dependencies

```
pip install -r requirements.txt
```

## 4. add supabase credentials

create a new file named .env in the project folder (same level as app.py and db.py).
paste your Supabase credentials:

```
SUPABASE_URL=https://yourproject.supabase.co
SUPABASE_KEY=your-service-role-key
```

## 5. run flask server

```
python app.py
```

if everything is correct, you’ll see:

```
* Running on http://127.0.0.1:5000
```

## 6. stop server

```
deactivate
```