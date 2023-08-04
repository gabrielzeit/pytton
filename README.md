# Pytton - website remote

Pytton is the simple hardware-side of a remote device for a website, used in production. Pytton was created with Python and CouchDB. 

### Naming story

"Pytton" is a mesh-up word from "Python" and "Button". 

### Concept

Pytton is a IOT project, where a webiste is controlled via a Raspberry Pi 3 Model 3+ and a joystick module. During the maufacturing process, a few plans are required to assemble a device. Pytton was invented for a more effiecient adjustment of the tabs.

### Technical devices

The project uses following hardware-devices.

- [Raspberry Pi 3 Model b+]
- [Ks0008 keyestudio Joystick Module]
- [KY-012 Active Piezo-Buzzer module]
- [KY-053 Analog digital converter]

### Technologies

The project uses following software.

- [Python3 version 3.7.3][python3]
- [CouchDB version 2.0][couchdb]
- [adafruit_ads1x15 library][adafruit]

### Programm functionality

#### Couchdb
The couchdb server should boot up automatically.
If the server is down, you have to start it yourself:

```sh
$ sudo -i -u couchdb /home/couchdb/bin/couchdb
```
Should an error occur, you have to update or reinstall the couchdb. Try:

```sh
$ sudo pip3 install couchdb
```
...for update. If even that can't make things right, you have to reinstall couchdb. Following these [instructions][couchdb].

If any other erros show up, try pdating the pychouchdb (the couchdb-extension for python):
```sh
$ sudo pip3 install pycouchdb
```
##### pychouchdb
Python Code for couchdb usement:

importing the library:
```
import pycouchdb
```
couchdb server hosting:
```
couch = pyouchdb.Server("http://localhost:5984/")
```
couchdb use/create database:
```
db = couch.database('joystick')
```
get object from database:
```
obj = db.get('dirID')
```
write object to databse:
```
obj = db.get('dirID')
obj['dir']=direction
db.save(obj)
```

#### Joystick
The sofware should start itself while booting. 
If an error appears, and the program does not start, you have to boot it up yourself:

```sh
$ sudo python3 /home/pi/Workplace/joystick/joystick.py
```

#### Adafruit Driver
The adafruit library should already be built in. In case of error, copy the library from the official [link][adafruit] and paste it right next to the 'joystick' script.

### Others
###### Comments 
There is more information about the code itself, in the joystick.py script, as comments. Within these comments, every part of the code is explained very precisely and should be unterstandable for everyone. 

###### Workflow
Pytton is the user-interaction side of a bigger project. Pytton delivers the motions of the joystick, and writes them into a database. This database contains just one object, which is updated with every move (it would be unneccesary to save all moves). The userinterface-side of the project reads this one line of the database (it listens at the changes) and if a change is done, the action on the screen happens. This interface-side's logic is written in JavaScript and displays the "results" in html5.
If a change in the database happens, only the direction and the id are stored (there is a few more couchdb-generated data but we don't use that one). The interface-side reads the direction and adjusts the tabs like the direction stored in the object.

###### Delay time
Pytton has a default delay time, between to moves, of 1 second to avoid hopping more than one tab at a moment. If the joystick is held in this direction, Pyton stores this move in the database every second.

###### CouchDB user-interface
There is also a userinterface for couchdb. It can be used for further investigation into teh database's structur and complexity.
The database server is hosted on localhost and the default port for coucdb 5984.
To get to the user interface, follow this link, when the server is hosted: 
http://localhost:5984/_utils/#/databse/joystick/_all_docs

###### Joystick signal
The joystick module delivers an analog signal, which can't be interpreted by the Raspberry Pi on its own. Therefore, a converter is needed, which translates the analog signal into a digital one. This is done through the [KY-053][KY-053 Analog digital converter] module from https://joy-it.net.

###### Buzzer
The buzzers purpose is to inform the user of the Pytton-remote, that he/she made an action. This is important because of the 1 secound of delay time. If the user is impatient or in a hurry, he/she is more likely to do multiple moves, when the result of their action isn't visible at the very first moment. Therefore, a buzzer signals the user that the remote got the input and is functionable.

###### Expandabilty
Pytton is expandable. At the first version of Pytton, 4 directions are caught and written into the database (up, down, right left). This version just uses right and left to hop from tab to tab.
The first expanable feature could be a scroll-function. If a document, displayed in a tab is realtively long, the user can scroll through the document like he/she could with a mousehweel.
The second extension would be to press the joystick. This event can be caught in python with the following command:
```
GPIO.input(Button_PIN)
```
The function for this action could be a switch to fullscreen mode of the document, or to zoom in a little bit.

[Raspberry Pi 3 Model b+]: <https://www.raspberrypi.org/products/raspberry-pi-3-model-b-plus/>
[Ks0008 keyestudio Joystick Module]: <https://wiki.keyestudio.com/index.php/Ks0008_keyestudio_Joystick_Module>
[KY-012 Active Piezo-Buzzer module]: <https://joy-it.net/en/products/COM-KY012APB>
[KY-053 Analog digital converter]: <https://joy-it.net/en/products/COM-KY053ADC>
[python3]: <https://www.python.org/downloads/release/python-373/>
[couchdb]: <https://andyfelong.com/2019/07/couchdb-2-1-on-raspberry-pi-raspbian-stretch/>
[adafruit]: <https://github.com/adafruit/Adafruit_Python_ADS1x15>
