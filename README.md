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


# After Installation Steps 

1) Create a new enviroment using the following command:
```bash
$ conda create -n mini-rag python=3.8
```
2) Activate the enviroment:
```bash
$ conda activate mini-rag