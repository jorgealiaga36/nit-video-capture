# NIT Camera Video Capturer

This proyect is an implementation of a video capturer of the NIT thermal camera called LIR320.

* For a more detailed information about the camera: https://www.lircameras.com/lir320/

## 1. Initial Configuration

1. Create (and activate) a new environment, named `nit-capt` with Python 3.9.

	- __Linux__ or __Mac__: 
	```
	conda create -n nit-capt python=3.9
	source activate nit-capt
	```
	- __Windows__: 
	```
	conda create --name nit-capt python=3.9
	activate nit-capt
	```

2. Clone current proyect repository and navigate to the downloaded folder.
```
git clone https://github.com/jorgealiaga36/nit-video-capture.git
cd nit-video-capture
```

3. Install required pip packages.
```
pip install -r requirements.txt
```

## 2. Usage

For running the code:

1. Make sure you are within the conda enviroment and the proyect directory previously cloned.
2. Run the following command:
```
~$ python video_capture.py --video-format [format] -output-source [recorded-video-root]
```

Where:
* `--video-format` or `-vf`: Video format selected (grayscale or corrected).

__Aclaration:__`Grayscale` - format records video in `.mkv` format and `corrected` format records video in `.RAW` format (specific video format given by the manufacturer).
* `--output-source` or `-ins`: Output recorded video root.

### 2.1. Intructions

Keys configurated for performing the following actions:

* Press `space-bar`: Start recording a new video. Press again for end recording.

__**You can record the videos you want.**__






