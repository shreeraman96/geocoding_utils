# geocoding_utils
### simple library with utility functions to use ARCGIS developer functions 

#### How to use: 
* Setup an ARCGIS online paid account	
*	clone this Repository to your local

##### features included for now:
* Geocode a single address
* Geocode an entire column of addresses in pandas dataframe 
* calculate road distance between two points 
		
	
### To setup the environment 

**To install Git**

Windows platform:
* use this link: https://git-scm.com/download/win
Mac or Ubuntu: 

```sudo apt install git-all```
or 
* use this link: https://git-scm.com/download/mac
	
using conda: 
	
```
  conda env create -f environment.yml
```
**To clone the repository to your local**
```
  git clone https://github.com/shreeraman96/geocoding_utils.git
```
**Before using the library configure the "config.yaml" file**
	
- replace ARCGIS online user id and password in the corresponding placeholder
		
**For calculating the road distance please configure your ARCGIS API application to get the client ID and client secret**
	
* To register an ARCGIS application follow step 1-4 in the following link:
		
    https://developers.arcgis.com/labs/rest/get-an-access-token/
			
* After getting the client ID and secret configure the "config.yaml" correspondingly
		
```
    arcAPICredentials:
			client_id: <client ID of registered application>
			client_secret: <client secret of registered application>
```				
### Follow the Sample jupyter notebook on how to use the library 

  geocode_esri.ipynb
	
		

