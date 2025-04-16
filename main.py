import os
import logging
import random
import time
from fastapi import FastAPI, Request, HTTPException, Header

app = FastAPI()
SECRET_KEY = os.getenv("SecretKey", "")
ENV = os.getenv("ENV", "dev")

log_level = os.getenv("LOG_LEVEL", "INFO").upper()  # Default to INFO if not set
log_format = os.getenv("LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")

logging.basicConfig(level=log_level, format=log_format)
logger = logging.getLogger("myapp")

logger.info(f"Running inside {ENV} environment")

@app.middleware("http")
async def log_request_time(request: Request, call_next):
	start_time = time.time()
	response = await call_next(request)
	end_time = time.time()
	duration = end_time - start_time
	logger.info(f"{response.status_code} | {request.method} {request.url.path} | {duration:.4f}s")
    
	return response

@app.get("/health")
async def health():
	return {"status": "success", "version": "v2"}

@app.get("/secret/access")
async def secure_access(request: Request, x_api_secret: str = Header(None)):
	if x_api_secret != SECRET_KEY and ENV != "prod":
		raise HTTPException(status_code=401, detail="unauthorized")

	return {"message": "Welcome to my secure route"}

@app.get("/heavy")
async def heavy():
	time.sleep(1)
	return {"message": f"response from heavy calculations {int(random.random() * 100 + 10000)}"}