FROM python:3
WORKDIR app
COPY . /app
RUN pip install -r Requirements.txt 
EXPOSE 8000
CMD ["python","manage.py","runserver","0.0.0.0:8000"]
