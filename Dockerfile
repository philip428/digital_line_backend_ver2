FROM continuumio/miniconda3

RUN mkdir /digital_line
COPY src/ /digital_line/
COPY ./environment.yml /digital_line/
WORKDIR /digital_line
# RUN apt-get update && apt-get install -y gcc
RUN conda env create -f ./environment.yml
SHELL ["conda", "run", "-n", "digital_line_backend", "/bin/bash", "-c"]

# RUN echo "source activate web" > ~/.bashrc
# ENV PATH /opt/conda/envs/web/bin:$PATH

# RUN chmod +x boot.sh

EXPOSE 5000

ENTRYPOINT ["conda", "run", "-n", "digital_line_backend", "flask", "run", "--host=0.0.0.0"]

# ENTRYPOINT ["./boot.sh"]
