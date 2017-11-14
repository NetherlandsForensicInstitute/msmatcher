LCMSweb
=======

## Basic requirements
* Node.js >= 6.x

For Ubuntu, install using
```bash
curl -sL https://deb.nodesource.com/setup_6.x > tmp
sudo ./tmp
sudo apt-get install -y nodejs
```

* Python >= 3.5

Required Python packages can be found in `requirements.txt`.


## Installation

To install the necessary Python packages, run:
```bash
pip install -r requirementst.txt
```

To install the requirements for the frontend, navigate to the directory `frontend` and run

```bash
npm install
```

## Configuration
* Copy `config.py.example` to `config.py`
* Fill in your details:
    - Database credentials
    - if you need to fill the database as well: file directories.



## Usage - Development
LCMSweb has three main components: *lcms*, *frontend* and *backend*. *lcms*
parses the data and puts it in a Postgresql database. *frontend* runs the
frontend part of the webapp. The *frontend* talks to the *backend* in order
to get data.


### lcms
???

Datamodel on Confluence.

### backend
To start the backend, run
```bash
python run_server.py
```
Running the backend is required to use the frontend.

### frontend
To start the frontend in development-mode, navigate to the directory `frontend` and run:
```bash
npm run dev
```
The frontend will be accessible from `http://localhost:8080`

For more information, see the readme included in the `frontend` directory.

## Usage - Deployment
Build the frontend from the directory `frontend` with:
```bash
npm run build
```

Start the flask server with from the main directory with:
```bash
python run_server.py
```
The webapp will be available at `http://localhost:5000`
