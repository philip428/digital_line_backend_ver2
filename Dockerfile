FROM continuumio/miniconda3

RUN mkdir /digital_line
COPY ./ /digital_line/
WORKDIR /digital_line
RUN apt-get update && apt-get install -y gcc
RUN conda env create -f ./environment.yml
RUN echo "source activate web" > ~/.bashrc
ENV PATH /opt/conda/envs/web/bin:$PATH

RUN chmod +x boot.sh

EXPOSE 5000

ENTRYPOINT ["./boot.sh"]