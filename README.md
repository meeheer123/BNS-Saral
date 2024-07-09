# BNS Saral

The goal of this project is to provide a simple way to convert the old laws to the corresponding new ones in India.

### Main Features

- Simple User Interface
- Intuitive Design
- Option to Get Additional Details About Each Section
- Procfile for Easy Deployments
- Separated Requirements Files

## Getting Started

### Prerequisites

Ensure you have the following installed:

- Python 3.x
- Git

### Installation

1. Clone the repository from GitHub and switch to the new directory:

   ```bash
   git clone https://github.com/meeheer123/BNS-Saral.git
   cd BNS-Saral
   ```
2. Activate the virtual environment for your project:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install project dependencies:

   ```bash
   pip install -r requirements.txt
   ```
4. Apply the migrations:

   ```bash
   cd src
   python manage.py migrate
   ```
5. Run the development server:

   ```bash
   python manage.py runserver
   ```

## Deployment

To deploy the project, make sure you have a `Procfile` set up for your deployment environment. Example content for `Procfile`:

    ``plaintext     web: gunicorn src.wsgi     ``

This setup assumes you are using Gunicorn for deployment. Adjust accordingly for your specific environment.

## Usage

Once the server is running, open your web browser and navigate to `http://127.0.0.1:8000` to access the application.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

---
