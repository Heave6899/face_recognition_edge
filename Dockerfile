ARG FUNCTION_DIR="/home/app/"
ARG RUNTIME_VERSION="3.8-slim"
ARG RUNTIME_VERSION_PYTHON="3.8"

FROM python:${RUNTIME_VERSION} AS python-alpine

# RUN apt-get update \
#     && apt-get install --no-install-recommends -y cmake ca-certificates libgl1-mesa-glx
# RUN python${RUNTIME_VERSION_PYTHON} -m pip install --upgrade pip

RUN apt-get update \
    && apt-get install --no-install-recommends -y cmake ca-certificates libgl1-mesa-glx \
    && apt clean 
    # && rm -rf /var/lib/apt/lists/*

RUN python${RUNTIME_VERSION_PYTHON} -m pip install --upgrade pip

FROM python-alpine AS build-image
ARG FUNCTION_DIR
ARG RUNTIME_VERSION
RUN mkdir -p ${FUNCTION_DIR}
RUN python${RUNTIME_VERSION_PYTHON} -m pip install --no-cache-dir awslambdaric --target ${FUNCTION_DIR}

FROM python-alpine
ARG FUNCTION_DIR
WORKDIR ${FUNCTION_DIR}
COPY --from=build-image ${FUNCTION_DIR} ${FUNCTION_DIR}
ADD https://github.com/aws/aws-lambda-runtime-interface-emulator/releases/latest/download/aws-lambda-rie /usr/bin/aws-lambda-rie
RUN chmod 755 /usr/bin/aws-lambda-rie
RUN apt-get install -y ffmpeg

COPY ./checkpoint ${FUNCTION_DIR}/checkpoint
COPY ./build_custom_model.py ${FUNCTION_DIR}/build_custom_model.py
COPY ./entry.sh /entry.sh
COPY ./eval_face_recognition.py ${FUNCTION_DIR}/eval_face_recognition.py
COPY ./handler.py ${FUNCTION_DIR}/handler.py
COPY ./requirements.txt ${FUNCTION_DIR}/requirements.txt
COPY ./__pycache__ ${FUNCTION_DIR}/__pycache__
COPY ./models ${FUNCTION_DIR}/models
# COPY ./IMG_20220417_163147.jpg ${FUNCTION_DIR}/IMG_20220417_163147.jpg
RUN pip install --no-cache-dir -r ${FUNCTION_DIR}/requirements.txt -f https://download.pytorch.org/whl/cpu/torch_stable.html
RUN chmod 777 /entry.sh
RUN ls /
RUN ls ${FUNCTION_DIR}/
RUN apt autoremove

ENTRYPOINT [ "/entry.sh" ]
CMD [ "handler.face_recognition_handler" ]