FROM pytorch/pytorch:2.5.1-cuda12.4-cudnn9-devel

ENV PYTHONUNBUFFERED=1

RUN groupadd -r user && useradd -m --no-log-init -r -g user user
USER user

WORKDIR /opt/app

COPY --chown=user:user requirements.txt /opt/app/
COPY --chown=user:user resources /opt/app/resources

# You can add any Python dependencies to requirements.txt or run any script to build your Python environment
RUN python -m pip install \
    --user \
    --no-cache-dir \
    --no-color \
    --requirement /opt/app/requirements.txt

COPY --chown=user:user infer.py /opt/app/

ENTRYPOINT ["python", "infer.py"]