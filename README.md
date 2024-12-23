<img src="logo.png" alt="Logo" width="300"/>

## Getting Started

Follow these instructions to get the project up and running on your local machine.

### Prerequisites

- Docker
- Docker Compose

### Setup

1. Clone the repository:
    ```sh
    git clone https://github.com/mehraj-vivasoft/auto-query.git
    cd auto-query
    ```

2. Rename the `.env.example` file to `.env` in the following directories:
    - `fastapi-agent`
    - `huduri`
    - `make-dataset`

3. Update the `.env` files with the necessary environment variables.

### Running the Application

To build and start the application, run the following command:
```sh
docker-compose up --build
```

### Accessing the Application

- Dataset Maker Frontend: [http://localhost:3000](http://localhost:3000)
- Backend: [http://localhost:8000](http://localhost:8000)

The application will automatically migrate the database and start the MSSQL server on its proper port.

### Endpoint to Query the Database

- POST - `/query` - Query the database in natural language. The request body should contain the query in the following format:
    ```json
    {
        "query": "How many types of holidays are there?"
    }
    ```
    The response will contain the result of the query.


### Stopping the Application

To stop the application, press `Ctrl+C` in the terminal where the application is running, then run:
```sh
docker-compose down
```

### Troubleshooting

If you encounter any issues, please check the logs for more details:
```sh
docker-compose logs
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

socat TCP-LISTEN:8000,fork TCP:127.0.1:8000