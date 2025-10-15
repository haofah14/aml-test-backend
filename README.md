## 1. clone repo

```
git clone https://github.com/haofah14/aml-test-backend
cd backend
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

create a new file named .env in the project folder (same level as app.py and db.py)

paste your Supabase credentials

supabase url can be found in project settings > data API > project URL

supabase key can be found in project settings > API keys > legacy API keys > service_role 

```
SUPABASE_URL=https://yourproject.supabase.co
SUPABASE_KEY=your-service-role-key
```

## 5. run flask server

```
python app.py
```

if everything is correct, you’ll see in the terminal:

```
 Flask server connected and running at http://127.0.0.1:5000
 * Serving Flask app 'app'
 * Debug mode: on
```

## 6. stop server

```
deactivate
```