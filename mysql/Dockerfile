FROM mysql:9.0.1

RUN microdnf update && \
  microdnf install glibc-langpack-ja -y && \
  microdnf clean all

ENV LANG ja_JP.utf8

COPY ./sql /docker-entrypoint-initdb.d
