# shrm_research
A Python environment, and collection of Jupyter Notebooks, to help the research team at SHRM fulfill its mission. 

## Installing the Docker image
1. Go to https://docs.docker.com/docker-for-windows/install/ and understand the process.  You may need to create a support ticket.
    A. Download the following from Git:  https://github.com/bgebert/shrm_research/archive/refs/heads/main.zip
    B. Extract the contents of the zip file
2. From a command prompt, or terminal wihndow, navigate to where you unzipped main.zip

#build container from jupyter/scipy-notebook:latest
docker build -t shrm_research .

# for the team
docker run --name research_app -it --volume '/Volumes/share/Departments/Research & Insights/Sampling':/home/jovyan/s_drive_sampling --volume '/Volumes/share/Departments/Research & Insights/Sampling/notebooks/bgebert':/home/jovyan/notebooks -p 8888:8888 shrm_research

# for Brad
docker run --name research_app -it --volume '/Volumes/share/Departments/Research & Insights/Sampling':/home/jovyan/sampling --volume '/Volumes/share/Departments/Research & Insights/Sampling/notebooks/bgebert':/home/jovyan/notebooks --volume ~/Scripts/SHRM/shrm_research/notebooks:/home/jovyan/source_notebooks -p 8888:8888 shrm_research