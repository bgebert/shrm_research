# shrm_research
A Python environment, and collection of Jupyter Notebooks, to help the research team at SHRM fulfill its mission. 

## Initial Steps
1. Open Windows Explorer to the S drive / Departments / Research & Insights / Sampling / notebooks
2. Create a new folder with your username.  For example, bgebert or tburner.  This username will be used below in the "for the team" section

## Installing and Creating the Docker image
1. Go to https://docs.docker.com/docker-for-windows/install/ and understand the process.  You may need to create a support ticket.
2. Download the following from Git:  https://github.com/bgebert/shrm_research/archive/refs/heads/main.zip
3. Extract the contents of the zip file
4. From a command prompt, or terminal wihndow, navigate to where you unzipped main.zip
5. docker build -t shrm_research . #build container from jupyter/scipy-notebook:latest

## Creating the Docker container (different steps depending on who is running it.)
# for the team
1. Open a command prompt and paste the following: docker run --name research_app -it --volume '/Volumes/share/Departments/Research & Insights/Market Research':/home/jovyan/market_research --volume '/Volumes/share/Departments/Research & Insights/Sampling':/home/jovyan/sampling --volume '/Volumes/share/Departments/Research & Insights/Sampling/notebooks/**your_username**':/home/jovyan/notebooks -p 8888:8888 shrm_research

# for Brad
1. Open a command prompt and paste the following: --volume '/Volumes/share/Departments/Research & Insights/Market Research':/home/jovyan/market_research --volume '/Volumes/share/Departments/Research & Insights/Sampling':/home/jovyan/sampling --volume '/Volumes/share/Departments/Research & Insights/Sampling/notebooks/bgebert':/home/jovyan/notebooks --volume ~/Scripts/SHRM/shrm_research/notebooks:/home/jovyan/source_notebooks -p 8888:8888 shrm_research

## Running Docker
1. Open a command prompt, and run: docker start research_app
2. Open Google Chrome and go to http://localhost:8888/tree?
