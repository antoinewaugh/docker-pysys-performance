FROM relativetechnologies/apama:latest

COPY . /perf

WORKDIR /perf
CMD ['pysys', 'run']
