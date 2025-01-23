# Build stage
FROM python:3.10-slim as builder

WORKDIR /app
COPY . .

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev && \
    pip install --user -r requirements.txt && \
    python setup.py sdist bdist_wheel

# Runtime stage
FROM python:3.10-slim

WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/locales ./locales
COPY --from=builder /app/resources ./resources

ENV PATH=/root/.local/bin:$PATH
ENV PYTHONPATH=/app

# Install package
RUN pip install --no-cache-dir dist/*.whl

# Set up entrypoint
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["run-app"]