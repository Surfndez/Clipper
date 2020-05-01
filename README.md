### Setup

#### Docker & Docker Compose
1) [Install Docker](https://docs.docker.com/get-docker/)
2) [Install Docker Compose](https://docs.docker.com/compose/install/)

#### Google Cloud Vision
1) Follow instructions [here](https://cloud.google.com/vision/docs/quickstart-client-libraries) to create a Google Cloud Vision Enabled Project and download `key.json`
2) Open the `env` file at the root of the project and make `WHERE_IS_MY_GOOGLE_CLOUD_PLATFORM_KEY_JSON_FILE` match where you downloaded your file.    

#### Twilio
0) Use the promo code DEVHACK20 for $20 when you create your account.
1) [Create a new Twilio Account](https://www.twilio.com/try-twilio?promo=Gbv52f) **(DISCLAIMER: this is my referral link)**
2) Navigate to your [Twilio Console](https://www.twilio.com/console) and copy your `ACCOUNT SID` and `AUTH TOKEN` into the same `.env` file from above.
3) Buy a Twilio phone number and copy it to your `pyclipper/pyclipper.ini.sample` file.  

**Finally, change the name of the `pyclipper.ini.sample` to `pyclipper.ini`**

#### Run Application

* Run `docker-compose up` (AFTER FOLLOWING SETUP INSTRUCTIONS)
    



# TODO
* ~~Get google application credentials into environemnt where its needed. I need to figure out docker for this~~

* ~~Automate `ngrok` and `twilio` webhook configuration~~

* ~~Install twilio cli into Docker Image~~

* Complete README

* Avoid Key Errors by crashing with warnings first

* ~~Remove env from git history and make .env.sample in Git~~

* ~~Fix Twilio not finding credentials~~

* Silence Rabbit output 




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

#### External Dependencies

* `docker` - easily deploy and run applications
* `nodemon` -  automatically restarting program when you make changes - https://nodemon.io/





* Install Dependencies 
    
    ```
    virtualenv .env && source .env/bin/activate && pip install -r requirements.txt
    ```

* Add stuff to pyclipper.ini.sample

* Change `pyclipper.ini.sample` to `pyclipper.ini` and fill in credentials

