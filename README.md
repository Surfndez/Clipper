### How To

#### Install Python Dependencies

    virtualenv .env && source .env/bin/activate && pip install -r requirements.txt


#### Run Tests

    nodemon -e py --exec "python -m unittest discover"


#### Run Application
* Create a Google Cloud Vision Enabled Project and Download `key.json`


    export GOOGLE_APPLICATION_CREDENTIALS="/your/key/path/[FILE_NAME].json"

* Install Dependencies 
    

    virtualenv .env && source .env/bin/activate && pip install -r requirements.txt

* Add stuff to pyclipper.ini.sample

* Change `pyclipper.ini.sample` to `pyclipper.ini` and fill in credentials

* Start RabbitMQ Server


    docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management

5) Start Message Consumer `worker.py`

#### External Dependencies

* `nodemon` -  automatically restarting program when you make changes - https://nodemon.io/
* `ngrok` - exposing localhost to all of your friends (and enemies) - https://dashboard.ngrok.com/get-started
* `docker`?