### How To

#### Install Python Dependencies

    virtualenv .env && source .env/bin/activate && pip install -r requirements.txt


#### Run Tests

    nodemon -e py --exec "python -m unittest discover"


#### Run Application
* Start ngrok and get URL
* Get a Twilio Number and add ngrok URL/sms to Twilio Number
LOOK HERE AND AUTOMATE THIS https://www.twilio.com/docs/twilio-cli/general-usage#webhooks
* Create a Google Cloud Vision Enabled Project and Download `key.json`

    ```
    export GOOGLE_APPLICATION_CREDENTIALS="/your/key/path/key.json"
    ```

* Install Dependencies 
    
    ```
    virtualenv .env && source .env/bin/activate && pip install -r requirements.txt
    ```

* Add stuff to pyclipper.ini.sample

* Change `pyclipper.ini.sample` to `pyclipper.ini` and fill in credentials

* Start RabbitMQ Server
    ```
    docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
    ```   

* Start Message Consumer 
    ```
    export GOOGLE_APPLICATION_CREDENTIALS="/your/key/path/key.json"
    python -m worker.worker
    ```
* Start Server
    ```
    export GOOGLE_APPLICATION_CREDENTIALS="/your/key/path/key.json"
    python -m server.server
    ```
    
#### External Dependencies

* `nodemon` -  automatically restarting program when you make changes - https://nodemon.io/
* `ngrok` - exposing localhost to all of your friends (and enemies) - https://dashboard.ngrok.com/get-started
* `docker`?




# ORGANIZE THIS HELPFUL STUFF

## Twilio
### First Time Setup
    brew tap twilio/brew && brew install twilio
    twilio login
    twilio autocomplete zsh
    printf "$(twilio autocomplete:script zsh)" >> ~/.zshrc; source ~/.zshrc
        
### Subsequent Changes    
    twilio phone-numbers:list 
    twilio phone-numbers:update YOUR_NUMBER --sms-url YOUR_URL/sms


# Problems
Get google application credentials into environemnt where its needed. I need to figure out docker for this
