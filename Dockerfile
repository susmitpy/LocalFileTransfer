# official python image 
FROM python:3.9-slim 

# setting working dir
WORKDIR /localfiletransfer

# copy flask app in to the container
COPY . /localfiletransfer

# installing requirements
RUN pip install --no-cache-dir -r requirements.txt

# exposing port 5000
EXPOSE 5000

# command to run the app
CMD [ "python3", "app.py" ]
