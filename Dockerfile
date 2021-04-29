FROM jupyter/scipy-notebook:latest

# reset user to root for installing additional packages
USER root

# reset container user to jovyan
#USER jovyan

# set the work directory
WORKDIR /home/jovyan

# make docker use bash instead of sh
SHELL ["/bin/bash", "--login", "-c"]

# Create the environment:
# NOTE: The presence of jupyter_notebook_config.json in the root dir is ... 
#       enough to surpress the token/pwd of jupyter notebooks
#COPY jupyter_notebook_config.json /opt/conda/etc/jupyter/jupyter_notebook_config.json
COPY jupyter_notebook_config.json .
COPY update_notebooks.ipynb .
COPY README.md .
COPY environment.yml .
COPY command.sh /bin

# remove directory created by jupyter/scipy-notebook image
RUN rm -rf work

RUN conda env create -f environment.yml

# Make RUN commands use the new environment:
SHELL ["conda", "run", "-n", "shrm_research", "/bin/bash", "-c"]

RUN echo "source activate shrm_research" > ~/.bashrc
ENV PATH /opt/conda/envs/shrm_research/bin:$PATH

#RUN conda install -y qgrid

RUN jupyter contrib nbextension install --sys-prefix
RUN jupyter nbextension enable collapsible_headings/main --sys-prefix
RUN jupyter nbextension enable toc2/main --sys-prefix
RUN jupyter nbextension enable skip-traceback/main --sys-prefix
RUN jupyter nbextension enable codefolding/main --sys-prefix
RUN jupyter nbextension enable scroll_down/main --sys-prefix
RUN jupyter nbextension enable toggle_all_line_numbers/main --sys-prefix

#RUN ipython kernel install --user --name=shrm_research     # configure Jupyter to use Python kernel

# Add Tini. Tini operates as a process subreaper for jupyter. This prevents kernel crashes.
#ENV TINI_VERSION v0.6.0
#ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /usr/bin/tini
#RUN chmod +x /usr/bin/tini
#ENTRYPOINT ["/usr/bin/tini", "--"]

# expose the public port we want to run on
EXPOSE 8888

#CMD ["jupyter", "notebook", "--port=8888", "--no-browser", "--ip=0.0.0.0", "--allow-root"]
ENTRYPOINT ["bash", "/bin/command.sh"]