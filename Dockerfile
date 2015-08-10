FROM tleyden5iwx/caffe-cpu-master

ADD . /code
RUN pip install -r /code/requirements.txt
CMD python /code/app.py
