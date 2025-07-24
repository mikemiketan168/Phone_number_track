### How to Run

## -- COPY THE CODE --
1. If you using Visual Studi Code (VSC) you can make file using Ctrl + n, and if you using terminal use this bash
```
nano track3.py
```

<img width="1095" height="622" alt="image" src="https://github.com/user-attachments/assets/1fd4830a-2de0-434e-941a-69841856e69f" />

2. Copy the code 

<img width="1096" height="613" alt="Screenshot 2025-07-24 125140" src="https://github.com/user-attachments/assets/0738cce0-d23f-47d6-9ee9-8044497290ff" />

3. Save the file using Ctrl + s then Ctrl + x for exit

-- API KEY --
1. First we need an API key to track our phone number. Open https://opencagedata.com/api#quickstart

 <img width="507" height="494" alt="image" src="https://github.com/user-attachments/assets/93eb04bb-a344-4913-abfa-69e027424429" />

2. Click "Sign up for your geocoding API key"

<img width="476" height="672" alt="image" src="https://github.com/user-attachments/assets/757ac614-eec4-4568-93ad-a516ae5fbe17" />

3. Go create an account, and fill with this data

<img width="594" height="573" alt="image" src="https://github.com/user-attachments/assets/e7def2d7-ffd7-4111-86f6-e5c070d62a2f" />

4. Never check "Phone number search" or it will be banned
5. Once you complete make account, go to Geocoding API tab

<img width="594" height="573" alt="Screenshot 2025-07-24 124130" src="https://github.com/user-attachments/assets/28071c3c-ca66-40ab-8680-f167b4fa1a7f" />

6. Copy the API key and replace with your own key

<img width="463" height="66" alt="image" src="https://github.com/user-attachments/assets/65e0a605-e577-4a70-beb8-985525353066" />


##-- INSTALATION REQUIRED --
1. Open terminal

<img width="1082" height="603" alt="image" src="https://github.com/user-attachments/assets/4444c258-75c9-4ad3-9d36-c2c1beea0273" />

2. Copy this bash code and enter
```
sudo apt update
sudo apt install python3
python3 -m pip install --user phonenumbers folium colorama pytz
```

##-- RUN THE PROGRAM --
1. Once you done with all the step, run using this bash. Change {your phone number} with your phone number
```
python3 ./track3.py -p +1234567891
```

<img width="832" height="536" alt="Screenshot 2025-07-24 125551" src="https://github.com/user-attachments/assets/675009fb-7af9-4e9b-9529-3723e59166c4" />
