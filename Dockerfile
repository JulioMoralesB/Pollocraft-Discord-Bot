FROM balenalib/raspberrypi4-64-python

ADD main.py .
ADD responses.py .
RUN pip install python-dotenv
RUN pip install discord
RUN pip install mcstatus

CMD ["python", "./main.py"]