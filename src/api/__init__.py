from fastapi import FastAPI
from api.GetCheckInComment import router as get_checkin_comment_router
import logging
logging.basicConfig(level=logging.INFO)
logging.info("API module loaded.")

app = FastAPI()


@app.get("/", tags=["health"])
def read_root():
	return {"status": "ok", "message": "Pega check-in comment service"}


@app.get("/health", tags=["health"])
def health():
	return {"status": "ok"}


app.include_router(get_checkin_comment_router)