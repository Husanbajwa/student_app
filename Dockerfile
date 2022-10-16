FROM python:3
COPY . .
RUN pip install -r Requirements.txt 
EXPOSE 8000
CMD ["python","manage.py","runserver","0.0.0.0:8000"]
