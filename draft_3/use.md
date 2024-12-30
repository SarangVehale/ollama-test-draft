# To install the required dependencies, you can use
'''
pip install -r requirements.txt
'''


# Optional considerations : 
    #1. Python version -> Python 3.8+
    #2. Virtual Environment -> 
            It's a good practice to use a virtual environment for managing dependencies. 
            
            Create Virtual Environment 
            '''
            python -m venv venv
            '''
            
            Activate environment (on Windows) : 
            '''
            venv\Scripts\activate

            Activate environment (on Mac/Linux) : 
            source venv/bin/activate

# Building and Running the Docker Container 

    #1. Building the Docker image 
        '''
        docker build -t data-pipeline .
        '''

    #2. Run the Docker Container 
        '''
        docker run -it --rm data-pipeline excel ./data/sample_file.xlsx
        '''
    
    #3. Testing your Docker Container 
        '''
        docker logs <container_id>

    ## You can find the container ID using : 
        '''
        docker ps -a
        '''

## (Optionally) Push Docker Image to Docker Hub 

    #1. Login to Docker Hub 
        '''
        docker login
        '''

    #2. Tag your image 
        '''
        docker tag data-pipeline yourusername/data-pipeline:latest

    #3. Push the image 
        '''
        docker push yourusername/data-pipeline:latest
        '''


# Clean up Docker Resources (Optional)

To list all containers :
    '''
    docker ps -a
    '''

To remove stopped containers : 
    '''
    docker container prune
    '''
    
To remove unused images : 
    '''
    docker image prune 
    '''

