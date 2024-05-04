from fastapi import FastAPI, Request, Form, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from skillixir.processor import KeywordsProcessor


app = FastAPI()

kw_processor = KeywordsProcessor()

# Directory for templates
templates = Jinja2Templates(directory='templates')

# Serve static files, assuming you have a 'static' directory for CSS/JS
app.mount('/static', StaticFiles(directory='static'), name='static')


@app.get('/', response_class=HTMLResponse)
async def read_index(request: Request):
	return templates.TemplateResponse('index.html', {'request': request})


@app.post('/get_result')
async def get_result(
	request: Request, position: str = Form(...), location: str = Form(...), file: UploadFile = File(...)
):
	# Process form data and file here
	# For now, just redirecting to the home page
	return templates.TemplateResponse('index.html', {'request': request})


@app.post('/upload')
async def upload(request: Request, file: UploadFile = File(...)):
	# pdf to resume text
	# get positions
	# extract keywords from resume
	# extract keywords from positions
	# compare keywords
	# return result
	pass


if __name__ == '__main__':
	import uvicorn

	uvicorn.run(app, host='0.0.0.0', port=8000)
