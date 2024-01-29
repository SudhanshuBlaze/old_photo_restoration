FROM registry.us-west-1.aliyuncs.com/modelscope-repo/modelscope:ubuntu22.04-cuda11.8.0-py310-torch2.1.0-tf2.14.0-1.10.0
ENV DEBIAN_FRONTEND=noninteractive

RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:${PATH}

WORKDIR ${HOME}/app

COPY --chown=1000 ./requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

COPY --chown=1000 . ${HOME}/app

ENV MODELSCOPE_CACHE=${HOME}/cache \
    PYTHONPATH=${HOME}/app \
    PYTHONUNBUFFERED=1 \
    GRADIO_ALLOW_FLAGGING=never \
    GRADIO_NUM_PORTS=1 \
    GRADIO_SERVER_NAME=0.0.0.0 \
    GRADIO_THEME=huggingface \
    SYSTEM=spaces
RUN mkdir -p /home/user/.cache/modelscope/modelscope_modules/ && touch /home/user/.cache/modelscope/modelscope_modules/__init__.py
CMD ["python", "app.py"]