FROM revolutionsystems/python:3.6.3-wee-optimized-lto
COPY requirements.txt /app/

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

EXPOSE 5000

ENTRYPOINT ["bash"]
CMD ["./start.sh"]
