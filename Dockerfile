FROM python:3
COPY . .
RUN pip install -r Requirements.txt 
CMD ["python","manage.py","runserver","0.0.0.0:8000","--noreload"]
