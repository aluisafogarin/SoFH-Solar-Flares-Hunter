---
title: 'Solar Flares Hunter (SoFH): A python software to download solar images and convert from fits to png files.'
tags:
    - Python
    - astronomy
    - solar flares
authours:
    - name: Ana Luísa Fogarin de Sousa Lima
    affiliation: 1
    - name: André Leon Sampaio Gradvohl
    affiliation: 2
date: 16 May 2022
---
# Sumary

The Sun is in constant activity and some events, such as solar flares or coronal mass ejection, releases energy into space that may have repercussions on Earth and demage satellites, communication and energy transmission equipment. Thereby, is essential to have ways to predict those events in order to minimize the consequences. Some researchs uses solar images and machine learning to analyze, classify and predict active regions of the Sun in order to detect events. In order that, there is a need to have a large amount of solar images, and the process to obtain all of them can be slow and manual. Also it is common to get solar images in FITS (Flexible Image Transport System) extension, being also important to convert them to other formats to viabilize the study based on image prediction.

# Statement of Need

The main pourpuse of this software is to turn easier and faster the process to download solar images in HMI Continnum, HMI Magnetograms, AIA1600 and AIA1700. The user needs to inform the parameters about the wanted image in a CSV file, there must be a date and time, but other informations such as type of the solar flare can be also informed and the download will use that to save the images in different folders. The download uses the drms @drms package to obtain the images from the Joint Science Operations Center (JSOC) @jsoc.

The software also make it possible to convert large amount of FITS files to PNG only by selecting the images to convert, all other configurations regarding parameters to convert will be automatically set up by the software according to the wavelenght of inserted image.

Besides using the software interface, more advanced users can run the download or conversion by command line.

> python main.py <flare_information.csv> <operation_number>

Being: 1 for download and 2 for image conversion.

# References
