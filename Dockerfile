FROM python:3.9

WORKDIR /src

COPY requirements.txt /src/

RUN pip install -r requirements.txt

COPY . /src/

# Add docker-compose-wait tool -------------------
ENV WAIT_VERSION 2.7.2
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/$WAIT_VERSION/wait /wait
RUN chmod +x /wait

# -------------- The part below is for kubernetis deployment---------------
# # expose port
# EXPOSE 8000

# # start app  
# CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]