# MINI-RAG-APP

This is a minimal implementation of the RAG model for question answering.

## Reqirements

- Python 3.8 or later 


# Installing Python using Miniconda

This guide will help you install Python 3.8 or later using Miniconda.

## What is Miniconda?

Miniconda is a minimal installer for conda, a package and environment manager. It includes Python and allows you to create isolated environments for different projects.

## Installation Steps

### Windows

1. Download the Miniconda installer from [https://docs.conda.io/en/latest/miniconda.html](https://docs.conda.io/en/latest/miniconda.html)
2. Run the downloaded `.exe` file
3. Follow the installation wizard:
   - Click "Next" through the setup screens
   - Accept the license agreement
   - Choose installation location (default is recommended)
   - **Important**: Check "Add Miniconda3 to my PATH environment variable" for easier access
4. Click "Install" and wait for completion
5. Open Command Prompt or Anaconda Prompt and verify installation:
   ```bash
   conda --version
   python --version
   ```

### macOS

1. Download the Miniconda installer from [https://docs.conda.io/en/latest/miniconda.html](https://docs.conda.io/en/latest/miniconda.html)
2. Open Terminal and navigate to the Downloads folder:
   ```bash
   cd ~/Downloads
   ```
3. Run the installer:
   ```bash
   bash Miniconda3-latest-MacOSX-x86_64.sh
   ```
   (Use `Miniconda3-latest-MacOSX-arm64.sh` for Apple Silicon Macs)
4. Follow the prompts:
   - Press Enter to review the license
   - Type "yes" to accept
   - Press Enter to confirm the installation location
   - Type "yes" when asked to initialize Miniconda3
5. Close and reopen Terminal, then verify:
   ```bash
   conda --version
   python --version
   ```

### Linux

1. Download the Miniconda installer:
   ```bash
   wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
   ```
2. Make the installer executable:
   ```bash
   chmod +x Miniconda3-latest-Linux-x86_64.sh
   ```
3. Run the installer:
   ```bash
   ./Miniconda3-latest-Linux-x86_64.sh
   ```
4. Follow the prompts (similar to macOS instructions)
5. Restart your terminal and verify:
   ```bash
   conda --version
   python --version
   ```

## Creating a Python Environment

After installation, create a new environment with Python 3.8 or later:

```bash
# Create environment with Python 3.11 (or specify your preferred version)
conda create -n myproject python=3.11

# Activate the environment
conda activate myproject

# Verify Python version
python --version
```

## Basic Conda Commands

```bash
# List all environments
conda env list

# Activate an environment
conda activate myproject

# Deactivate current environment
conda deactivate

# Install packages
conda install package-name

# Remove an environment
conda remove -n myproject --all
```

## Troubleshooting

- If `conda` command is not found, restart your terminal or add Miniconda to your PATH manually
- On Windows, use "Anaconda Prompt" instead of Command Prompt if you encounter issues
- For permission errors on macOS/Linux, avoid using `sudo` with conda commands

## Additional Resources

- [Conda Documentation](https://docs.conda.io/)
- [Conda Cheat Sheet](https://docs.conda.io/projects/conda/en/latest/user-guide/cheatsheet.html)


## After Installation Steps 

1) Create a new enviroment using the following command:
```bash
$ conda create -n mini-rag python=3.8
```
2) Activate the enviroment:
```bash
$ conda activate mini-rag
```
3) Install the required packages
```bash
$ pip install -r requirements.txt
```
4) Setup the enviroment variables
```bash
$ cp .env.example .env
```
Set your enviroment variables in the `.env` file. Like `OPENAI_API_KEY` value

## Run the FastAPI server

```bash
# Start the FastAPI server using Uvicorn
$ uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Breakdown of the Command

- **`uvicorn`**: This is the ASGI server that will run your FastAPI application. It's lightweight and designed for high performance.

- **`main:app`**: 
  - **`main`**: This refers to the Python file (`main.py`) where your FastAPI application instance is defined.
  - **`app`**: This is the FastAPI application instance created in the `main.py` file. Make sure it looks something like this:
    ```python
    from fastapi import FastAPI
    
    app = FastAPI()
    ```

- **`--reload`**: This flag enables the automatic reloading of the server when code changes are detected. It's particularly useful during development, as it allows you to see changes without needing to restart the server manually.

- **`--host 0.0.0.0`**: This specifies that the server should be accessible from any IP address. If you want your server to be reachable from outside your local machine (like on a network), this option is necessary.

- **`--port 8000`**: This sets the port number on which your FastAPI application will run. Port `8000` is a common choice for development, but you can change it to any available port.

### Example Usage

1. Ensure you have FastAPI and Uvicorn installed:
   ```bash
   pip install fastapi uvicorn
   ```

2. Save your FastAPI application in a file named `main.py`.

3. Run the command in your terminal to start the server.

### Accessing Your API

- After starting the server, you can access your FastAPI application by navigating to `http://localhost:8000` in your web browser or using tools like Postman or curl.

### Additional Commands

- To see the automatically generated API documentation, visit:
  - **Swagger UI**: `http://localhost:8000/docs`
  - **ReDoc**: `http://localhost:8000/redoc`

## Installing Docker
 
Docker is required to run the MongoDB service for this project.
 
### Windows & macOS
 
1. Download **Docker Desktop** from [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)
2. Run the installer and follow the setup wizard
3. Launch **Docker Desktop** from your Applications or Start Menu
4. Wait for the Docker engine to start (the whale icon in your taskbar/menu bar will stop animating)
5. Verify the installation:
 
```bash
docker --version
docker compose version
```
 
> **Windows users:** Docker Desktop requires WSL 2 (Windows Subsystem for Linux). The installer will prompt you to enable it automatically if it isn't already.
 
### Linux
 
```bash
# Update package index
sudo apt-get update
 
# Install dependencies
sudo apt-get install ca-certificates curl gnupg
 
# Add Docker's official GPG key
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
 
# Add Docker repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
 
# Install Docker Engine
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
 
# Allow running Docker without sudo (optional but recommended)
sudo usermod -aG docker $USER
newgrp docker
 
# Verify
docker --version
docker compose version
```
 
> **Note:** After adding your user to the `docker` group, you may need to log out and back in for the change to take effect.
 
---

## Installing MongoDB Compass
 
**MongoDB Compass** is the official GUI for MongoDB. It lets you visually browse your collections, run queries, and inspect documents — very useful for debugging your RAG data.
 
### Windows
 
1. Go to [https://www.mongodb.com/try/download/compass](https://www.mongodb.com/try/download/compass)
2. Select **Windows**, choose the latest stable version, and click **Download**
3. Run the downloaded `.exe` installer
4. Follow the setup wizard (default options are fine)
5. Launch **MongoDB Compass** from the Start Menu
 
### macOS
 
1. Go to [https://www.mongodb.com/try/download/compass](https://www.mongodb.com/try/download/compass)
2. Select **macOS** and download the `.dmg` file
3. Open the `.dmg` and drag **MongoDB Compass** into your Applications folder
4. Launch it from Applications
 
Alternatively, install via Homebrew:
 
```bash
brew install --cask mongodb-compass
```
 
### Linux (Ubuntu/Debian)
 
```bash
# Download the .deb package
wget https://downloads.mongodb.com/compass/mongodb-compass_1.44.0_amd64.deb
 
# Install it
sudo dpkg -i mongodb-compass_1.44.0_amd64.deb
 
# Launch
mongodb-compass
```
 
> Check the [official downloads page](https://www.mongodb.com/try/download/compass) for the latest version number.
 
### Connecting Compass to Your Local MongoDB
 
Once MongoDB is running via Docker Compose, open Compass and connect using:
 
```
mongodb://localhost:27017
```
 
Or if you've set a username/password in your `.env`:
 
```
mongodb://username:password@localhost:27017
```
 
From there you can browse the `mini_rag_db` database, inspect your `projects` and `data_chunks` collections, and verify that your documents are being stored and chunked correctly.
 
---


## Run Docker Compose Services

```bash
 $ cd docker
 $ cd .env.example  .env

 - update `env` with your credentials
 ```

```bash
 $ cd docker
 $ sudo docker compose up -d
```