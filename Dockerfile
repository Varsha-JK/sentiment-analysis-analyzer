FROM python:3.9
RUN mkdir /app
ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 7007
CMD ["python", "app.py"]