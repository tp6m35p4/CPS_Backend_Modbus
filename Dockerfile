FROM python:3.7-alpine3.7

COPY . /app
WORKDIR /app
RUN pip install -r requirement.txt
RUN export FLASK_APP=main.py
EXPOSE 5000
ENTRYPOINT [ "flask" ]
CMD ["run", "--host=0.0.0.0"]