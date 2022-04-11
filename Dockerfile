FROM python:3.9
WORKDIR /code
COPY requirements.txt requirements.txt
# RUN apt-get -y update
# RUN apt-get install -y ffmpeg
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN chmod +x main.py
CMD [ "python", "main.py" ]