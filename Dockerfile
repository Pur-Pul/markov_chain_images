FROM python:3.8
EXPOSE 8080
WORKDIR /usr/src/app
COPY . .
RUN pip install -r requirements.txt
CMD invoke start --web