FROM python:3.11-slim

WORKDIR ./

COPY requirements/prd.txt ./requirements.txt
#COPY requirements/prd.txt ./requirements.txt # this works

RUN pip3 install -r requirements.txt

COPY . .

# suggested workers is 2*Core+1
# https://docs.gunicorn.org/en/latest/design.html#how-many-workers
# CMD ["gunicorn", "snaptron_query.app.main_dash_app:server", "--workers=3", "--threads=3", "-b", "0.0.0.0:80"]

#Use below lines for kubernetes
ENTRYPOINT ["gunicorn"]
CMD ["snaptron_query.app.main_dash_app:server"]