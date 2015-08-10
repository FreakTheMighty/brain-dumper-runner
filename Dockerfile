FROM tleyden5iwx/caffe-cpu-master

ADD . /code
RUN pip install -r /code/requirements.txt
RUN mkdir -p /brain/inputs
CMD python /code/app.py
