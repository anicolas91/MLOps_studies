FROM agrigorev/zoomcamp-model:mlops-2024-3.10.13-slim

RUN pip install -U pip
RUN pip install pipenv

COPY ["Pipfile","Pipfile.lock","./"]

RUN pipenv install --system --deploy

COPY ["starter.py","./"]

ENTRYPOINT [ "python", "starter.py", "2023", "5"]

#EXPOSE 9696

#ENTRYPOINT ["gunicorn","--bind=0.0.0.0:9696","predict:app"]
