# Financial APP
## Introduction
This is the **Financial APP** backend implementation for the fullfillment of the take home assignment task by [CTW](https://ctw.inc/).

## Tech stacks
This implementation is written by **Python 3** with **Django** framework; The database used is **SQLite**. The reason for using Django is because Django is the backend framework that I am most familiar with; The reason for use SQLite as database is because that Django uses SQLite as its default database and SQLite is able to handle simple database tasks.
Please also make sure you have **Docker** installed as it is used for containerization in this project.

## Get started
1. Go to https://www.alphavantage.co/support/#api-key to get an `ALPHAVANTAGE_API_KEY`
2. In the root directory of this project, change the `.env_example` file to `.env` and modify its content to replace the `ALPHAVANTAGE_API_KEY` with yours key.
3. Open termianal in the root directory, run the following command:
    ```
    docker-compose build
4. Then run:
    ```
    docker-compose up -d
5. Find the docker image and then open the interactive terminal:
    ```
    docker exec -it <container image> bash
6. In the interactive terminal, run the following commands to run the database migrations:
   ```
   python financial/manage.py makemigrations
   python financial/manage.py migrate
7. [For Task 1] Run the following command to fetch the financial data:
   ```
   curl -X GET "http://localhost:5000/api/financial_data?start_date=2023-01-01&end_date=2023-01-14&symbol=IBM&limit=3&page=2"
   ```
   Feel free to change the above parmeters for more tests.
8. [For Task 2] Run the following command to do data manupulations for showing financial data and get statistics.
   ```
    curl -X GET "http://localhost:5000/api/statistics?start_date=2023-01-01&end_date=2023-01-31&symbol=IBM"
    ```
    Feel free to change the above parmeters for more tests.

## Notes
Due to limited time by personal reasons (Get infected with COVID), the containerization operations have not been tested by myself. Therefore, if the docker commands fail, please install all the dependancies by yourself and replace **step 3-5** in the above guides by the following command:
    ```
    python /financial/manage.py runserver 5000
    ```
Other steps are the same.

## Discussions
This implementaion could be improved in the following aspects:
1. Refactoring the exsiting code in terms of code structure, code quality and method implemenation.
2. Write more detailed README and add more inline comments to the codes.
3. More tests to cover edge cases.

Regarding the `ALPHAVANTAGE_API_KEY` storage, in local environment, we could directly use the method provided in this implementation. While in prodution environment, we could use secrets managers such as **AWS Secrets Manager** or **Bitwarden** to manage API keys.