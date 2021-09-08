# Mutant Api
This api has the objective to get a DNA like this **["ATGCGA", "CAGTGC", "TTATGT", "AGAAGG", "CCCCTA", "TCACTG"]** and check if this DNA is from a **mutant** or a **human**

If you want to test without clone the repository here the link to test in browser (Test in browser)[https://mutant-api-wbj4lkqt6a-ue.a.run.app/docs] or just the link to test with the postman https://mutant-api-wbj4lkqt6a-ue.a.run.app

#
## The Api
The api is built with: 

### API
1.  [*fastAPI*](https://fastapi.tiangolo.com/)
1.  [*uvicorn*](https://www.uvicorn.org/)
1.  [*gunicorn*](https://gunicorn.org/)
1.  [*pydantic*](https://pydantic-docs.helpmanual.io/)

### DB
1.  [*alembic*](https://alembic.sqlalchemy.org/en/latest/)
1.  [*sqlalchemy*](https://www.sqlalchemy.org/)
1.  [*psycopg2-binary*](https://pypi.org/project/psycopg2-binary/)

### Test
1.  [*pytest*](https://docs.pytest.org/en/6.2.x/)
1.  [*pytest-asyncio*](https://github.com/pytest-dev/pytest-asyncio)
1.  [*httpx*](https://github.com/encode/httpx)
1.  [*asgi-lifespan*](https://pypi.org/project/asgi-lifespan/)


#

## Running the API
You can run the mutant api with two ways:

1.  Docker for this you will need docker installed in your machine [Docker](https://www.docker.com/)

        docker-compose up -d --build
    
    then

        docker-compose up

    This will put the api and database online.
    You'll need to migrate the database to create the DNA table and Statistics table doing this:


        docker ps

    You should see an output that starts with something that looks like the following:
    
    CONTAINER ID | IMAGE
    ------------ | -----
    a123bc007edf | mutant_api
    867g5309hijk | mutant_db

    Copy the ID of the container running our server. In this example that would be a123bc007edf. Now we can start executing bash commands as the container's root use by typing:

        docker exec -it a123bc007edf bash
    then

        alembic upgrade head

    with this and I believe you should be fine and start to using the api in this url **localhost:8000** if you want to see the docs(OpenAPI) **localhost:8000/docs**

1.  Open the project in you preferred IDE Pycharm or VSCode, create a virtual enviroment [Creation of virtual environments](https://docs.python.org/3/library/venv.html) then run:
    
        pip install -r requirements.txt

    You can run:
        
        docker-compose up -d db

    To instantiate the Postgre or download and install in your local machine after that just run:

        alembic upgrade head
    to create all tables you guys need, after that you can run from you IDE or from your terminal with the VENV activated 

        uvicorn api.server:app --reload

#

## Test the API
Well you can test the mutant api with two ways as well no surprises I hope:

1.  These are the commands you need and you see above
    
    The **docker-compose up** you only need if your docker instance is down otherwise skip this one

        docker-compose up
        docker ps
        docker exec -it a123bc007edf bash
        pytest -v
    
    The only thing new here is the **pytest -v** this will run all the test are in the test folder.

1.  You can open the project in PyCharm or VSCode or the IDE your like but I know these two has support for test and configure their tests
    1. [Pytest on Pycharm](https://www.jetbrains.com/help/pycharm/pytest.html)
    1. [Pytest on VSCode](https://code.visualstudio.com/docs/python/testing)

    Or you can open you terminal go to the project folder and run

        pytest -v

    You only need to make sure if you install the dependencies in a venv has activated then.