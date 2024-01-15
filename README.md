# social-network
Simple set of REST APIs to operate users, that can perform various actions on posts that they create

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Swagger Documentation](#swagger-documentation)
- [Linting](#linting)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/staaceyD/social-network
   ```

2. Install dependencies and activate virtural env:

    ```bash
    poetry install
    poetry shell
    ```

3. Make sure you are in the main folder, i.e. 'social_network' and apply database migrations:
    
    ```bash
    python manage.py migrate
    ```

## Usage

Run the development server:
    
    ```bash
    python manage.py runserver
    ```

Your APIs will be accessible at http://127.0.0.1:8000/.

## API Endpoints

The full list of endpoints can be found in `openapi.yml` file

## Swagger Documentation

The Swagger documentation for this API is generated using drf-spectacular.

Visit the Swagger UI at: http://127.0.0.1:8000/schema/swagger-ui/

To download the schema visit http://127.0.0.1:8000/schema

Or, explore the JSON schema at: http://127.0.0.1:8000/schema/swagger/?format=openapi

To generate updated file use the following command:

```bash
python manage.py spectacular --color --file openapi.yml
```

## Linting

It's highly recommended that you install the pre-commit hook - this will
automatically lint your code each time you commit.

From the root of the project do this:

brew install pre-commit
pre-commit install