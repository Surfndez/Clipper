### Setup

#### Docker & Docker Compose
1) [Install Docker](https://docs.docker.com/get-docker/)
2) [Install Docker Compose](https://docs.docker.com/compose/install/) (if you need don't have it)

#### Google Cloud Vision
1) Follow instructions [here](https://cloud.google.com/vision/docs/quickstart-client-libraries) to create a Google Cloud Vision Enabled Project and download `key.json`
2) Open the `env` file at the root of the project and make `WHERE_IS_MY_GOOGLE_CLOUD_PLATFORM_KEY_JSON_FILE` match where you downloaded your file.    

#### Twilio
1) [Create a new Twilio Account](https://www.twilio.com/try-twilio?promo=Gbv52f) **(DISCLAIMER: this is my referral link)**
2) Navigate to your [Twilio Console](https://www.twilio.com/console) and copy your `ACCOUNT SID` and `AUTH TOKEN` into `pyclipper/pyclipper.ini.sample`
3) Buy a Twilio phone number and copy it to your `pyclipper/pyclipper.ini.sample` file.  

**Finally, change the name of the `pyclipper.ini.sample` to `pyclipper.ini`**

#### Run Application

* Run `docker-compose up` (AFTER FOLLOWING SETUP INSTRUCTIONS)
    
#### External Dependencies

* `docker` - easily deploy and run applications
* `nodemon` -  automatically restarting program when you make changes - https://nodemon.io/
* `ngrok` - exposing localhost to all of your friends (and enemies) - https://dashboard.ngrok.com/get-started





# TODO
* ~~Get google application credentials into environemnt where its needed. I need to figure out docker for this~~

* Automate `ngrok` and `twilio` webhook configuration

* Complete README



---
# ORGANIZE THIS HELPFUL STUFF
#### Install Python Dependencies

    virtualenv env && source env/bin/activate && pip install -r pyclipper/requirements.txt


#### Run Tests

    nodemon -e py --exec "python -m unittest discover"

## Twilio
### First Time Setup
    brew tap twilio/brew && brew install twilio
    twilio login
    twilio autocomplete zsh
    printf "$(twilio autocomplete:script zsh)" >> ~/.zshrc; source ~/.zshrc
        
### Subsequent Changes    
    twilio phone-numbers:list 
    twilio phone-numbers:update YOUR_NUMBER --sms-url YOUR_URL/sms




## Organize Later
* Get a Twilio Number and add ngrok URL/sms to Twilio Number
LOOK HERE AND AUTOMATE THIS https://www.twilio.com/docs/twilio-cli/general-usage#webhooks

* Install Dependencies 
    
    ```
    virtualenv .env && source .env/bin/activate && pip install -r requirements.txt
    ```

* Add stuff to pyclipper.ini.sample

* Change `pyclipper.ini.sample` to `pyclipper.ini` and fill in credentials

