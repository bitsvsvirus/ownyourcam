# OwnYourCam :sunglasses: :video_camera:


## 1. Motivation / Problem
In times of Covid-19, many companies, institutions and courses rely on remote measures. Therefore, more and more communication tools are used to replace physical communication with virtual communication. School lessons, university seminars, lectures, conferences and also customer meetings are outsourced to tools like Zoom, Skype, Microsoft-Teams or Slack. The danger of losing aspects of privacy through audio and video communication is higher in times like these. Through video communication, for example, conclusions can be drawn about the life situation of the participants: The living room, bedroom and even family members can be unintentionally part of the video clip.

<img src="https://i.imgur.com/AcEx6DU.png" width="200"/>

## 2. Solution
As the name suggests, we propose a solution that enables the participants of video conferences to have more control over their webcam. 'OwnYourTool'is compatible with any communication software (Zoom, Skype, Microsoft-Teams Slack and many more). It creates a virtual cam device where the participant can be seen but his background can be replaced with a virtual background. This video input device can then be selected as a webcam device by communication tools. This protects the privacy of the participants, even if the communication tool does not have the function of displaying a virtual background like "Zoom.us". Furthermore, it also provides more security if the communication tool is compromised, since the insertion of a virtual background is not handled within communication tools.

It is important to us to make this tool open-source to maintain transparency and trust.

### 2.1 Acknowledgement
A big thank you goes to the creator of the package 'pyfakewebcam' who ported the v4l2 package from python2 to python3, which was very useful for our project.
* https://github.com/jremmons/pyfakewebcam

## 3. Supported Platforms
- Linux Based Systems (tested on Ubuntu & Debian)
- Mac (in development)
- Windows (in development)

## 4. TL; DR
- Simple to use
- Creates a video device with protected modified video stream (see above), which can be selected by software as camera.
- Adds a virtual background to protect the privacy of the user.
- Is communication tools independent and therefore compatible with any communication software.


## 5. Setup / Installation
As mentioned above, the following steps are ONLY written for Linux-Systems.

### Prerequisites
1. Linux-based system (Ubuntu, Debian, Arch, ...)
2. Python3
3. NodeJs (recommended v12.16.2) or Docker
4. Ubuntu package 'v4l2loopback-utils' to create a virtual video-device on hosts:
```
    sudo apt-get install v4l2loopback-utils
```
5. Create a virtual-webcam device:
```
    modprobe v4l2loopback devices=1
```

### Dependencies
Clone and install repository specific dependencies.
```bash
    git clone git@github.com:bitsvsvirus/ownyourcam.git
    pip install -r requirements.txt
```
Please follow step 1 or step 2 described above.
- STEP 1: If you have node installed locally and would like to install node-dependencies locally.
```bash
    cd ownyourcam/bodypix-api && npm install
```
- STEP 2: (recommended) If want to use Docker.
``` bash
    docker pull quving/bodypix:latest
```

### Launch
To be able use that tool, you need to run 2 services in total. 
- Service 1 is javascript-based service that is responsible to distinguishing the foreground (you) from the background you would like to protect from recording using AI. 
- Service 2 streams the modified video-stream to the virtual-device created by the command above (Prerequisites).
#### Service 1
If you have followed STEP 1 at the installation steps, do this:
```bash
    cd ownyourcam/bodypix-api && node app.js
```
else (if you chose step 2):
``` bash
    docker run -it --rm -d -p 9000:9000 quving/bodypix:latest
```

#### Service 2
Run python-script.
```
python3 ownyourcam.py
```

Now your virtual-cam-device has been created and should be visible to communication-tools. 


Happy meeting! :heart:

