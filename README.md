# Simple FastAPI Sample API

This project contains a small FastAPI app for testing:

- GET
- POST
- PUT
- PATCH

Swagger UI is enabled by default and is available at:

http://127.0.0.1:8000/docs

## Install dependencies

```bash
pip install -r requirements.txt
```

## Run the API

```bash
uvicorn app:app --reload
```

Or run directly:

```bash
python app.py
```

## Example endpoints

- GET /items
- GET /items/1
- POST /items
- PUT /items/1
- PATCH /items/1
