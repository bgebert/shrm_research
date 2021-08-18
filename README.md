# shrm_research
A Python environment, and collection of Jupyter Notebooks, to help the research team at SHRM fulfill its mission. 

## Installing the Docker image
1. Open Windows Explorer to the S drive / Departments / Research & Insights / Sampling / notebooks
2. Create a new folder with your username.  For example, bgebert or tburner.  This username will be used below in the "for the team" section
3. Go to https://docs.docker.com/docker-for-windows/install/ and understand the process.  You may need to create a support ticket.
4. Download the following from Git:  https://github.com/bgebert/shrm_research/archive/refs/heads/main.zip
5. Extract the contents of the zip file
6. From a command prompt, or terminal wihndow, navigate to where you unzipped main.zip
7. docker build -t shrm_research . #build container from jupyter/scipy-notebook:latest

# for the team
docker run --name research_app -it --volume '/Volumes/share/Departments/Research & Insights/Market Research':/home/jovyan/market_research --volume '/Volumes/share/Departments/Research & Insights/Sampling':/home/jovyan/sampling --volume '/Volumes/share/Departments/Research & Insights/Sampling/notebooks/**your_username**':/home/jovyan/notebooks -p 8888:8888 shrm_research

# for Brad
--volume '/Volumes/share/Departments/Research & Insights/Market Research':/home/jovyan/market_research --volume '/Volumes/share/Departments/Research & Insights/Sampling':/home/jovyan/sampling --volume '/Volumes/share/Departments/Research & Insights/Sampling/notebooks/bgebert':/home/jovyan/notebooks --volume ~/Scripts/SHRM/shrm_research/notebooks:/home/jovyan/source_notebooks -p 8888:8888 shrm_research
