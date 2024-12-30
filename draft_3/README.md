**Project Usage Guide**

This guide explains how to use the project, from setting up the environment to running the program. It also includes steps to use the Dockerized version for seamless deployment.

---

## **Table of Contents**
1. [Prerequisites](#prerequisites)
2. [Setup Instructions](#setup-instructions)
3. [Running the Project](#running-the-project)
4. [Using Docker](#using-docker)
5. [Testing and Debugging](#testing-and-debugging)
6. [Cleanup](#cleanup)

---

### **1. Prerequisites**
- **Python 3.9+**
- **pip**: Python package manager
- **Tesseract OCR** (for OCR functionality):
  - Install via package manager:
    - Ubuntu: `sudo apt-get install tesseract-ocr`
    - macOS: `brew install tesseract`
    - Windows: Download from [here](https://github.com/tesseract-ocr/tesseract)
- **Docker**: For containerized deployment (optional).

---

### **2. Setup Instructions**

#### **Step 1: Clone the Repository**
Clone the repository to your local machine:
```bash
git clone <repository_url>
cd <repository_name>
```

#### **Step 2: Install Python Dependencies**
Set up a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Install required packages:
```bash
pip install -r requirements.txt
```

#### **Step 3: Configure the Application**
Update the `config.json` file to include any specific configurations for your environment:
```json
{
    "input_directory": "./data/",
    "output_directory": "./output/",
    "tesseract_path": "/usr/bin/tesseract"  # Adjust based on your installation
}
```

---

### **3. Running the Project**
Run the main script to start the pipeline:
```bash
python main.py
```

The program will prompt you to:
1. Select the data type (e.g., Excel, PDF, OCR, etc.).
2. Provide the file path.
3. Specify the type of analytics or inference you need.

#### **Example Command**:
```bash
python main.py
# Select: "Excel"
# Path: "./data/sample_file.xlsx"
# Analytics: "Summarize by column"
```

---

### **4. Using Docker**

#### **Step 1: Build the Docker Image**
Ensure Docker is installed and running. Then, build the Docker image:
```bash
docker build -t data-pipeline .
```

#### **Step 2: Run the Docker Container**
Run the container with interactive input:
```bash
docker run -it --rm data-pipeline
```

The program will prompt you for the data type, file path, and analytics type as it does in the local setup.

#### **Optional: Mount Local Directories**
If you want to access files from your local system, mount the directories:
```bash
docker run -it --rm -v $(pwd)/data:/app/data -v $(pwd)/output:/app/output data-pipeline
```
This will ensure your `data` and `output` directories are shared between your local system and the container.

---

### **5. Testing and Debugging**

#### **Testing the Scripts**
You can run individual scripts for debugging:
- **File Processing**:
  ```bash
  python file_processing.py
  ```
- **Data Cleaning**:
  ```bash
  python data_cleaning.py
  ```
- **Inference and Analytics**:
  ```bash
  python inference_and_analytics.py
  ```

#### **Logging**
Logs are saved in `logs/app.log`. Review them for errors or debugging information.

---

### **6. Cleanup**

#### **Python Environment Cleanup**
To remove unused dependencies and clean the environment:
```bash
pip freeze | xargs pip uninstall -y
```

#### **Docker Cleanup**
Remove unused Docker containers and images:
- List containers:
  ```bash
  docker ps -a
  ```
- Remove stopped containers:
  ```bash
  docker container prune
  ```
- Remove unused images:
  ```bash
  docker image prune
  ```

---

By following these instructions, you can efficiently set up, run, and deploy the project in both local and containerized environments. If you encounter any issues, consult the logs or the provided error messages for troubleshooting.



