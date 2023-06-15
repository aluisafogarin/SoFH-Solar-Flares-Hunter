---
title: 'Solar Flares Hunter (SoFH): A python software to download solar images and convert from fits to png files.'
tags:
  - Python
  - astronomy
  - solar flares
authors:
  - name: Ana Luísa Fogarin de Sousa Lima
    affiliation: 1
    corresponding: true
  - name: André Leon Sampaio Gradvohl
    orcid: 0000-0002-6520-9740
    corresponding: true
    affiliation: 1
affiliations:
 - name: School of Technology, University of Campinas, Brazil
   index: 1
date: 16 May 2022
---
# Sumary
The Sun is in constant activity. Some phenomena occurring on the Sun, such as solar flares or coronal mass ejection, release energy into space, which may have repercussions on Earth. Those phenomena can damage satellites, communication, and energy transmission equipment. Therefore, it is essential to have ways to forecast those events to minimize the consequences. Some research uses solar images and machine learning to analyze and classify active regions of the Sun to predict solar flares. 

One strategy to forecast solar flares is using Deep Learning methods to analyze the solar images. However, such a task requires an extensive dataset of solar images to train the Deep Learning models. To gather those images can be a slow and manual process. In addition, it is common to get solar images in Flexible Image Transport System (FITS) format, which is difficult to handle in Deep Learning software. 

Therefore, to help researchers collect sun images from the main datasets and convert them into the most suitable format for their image analysis and treatment software, we propose the Solar Flares Hunter (SoFH). SoFH is a python software to download solar images and convert them from FITS to PNG formats.

# Statement of Need

The main goal of SoFH software is to facilitate and accelerate the process of downloading solar images in the most common wavelengths: HMI Continuum, HMI Magnetograms, AIA1600, and AIA1700. For that task, the user needs to inform the parameters about the wanted image in a CSV file. The necessary parameters are date and time, but the user can provide other information, such as the type of the solar flare. The software will download and save the images in different folders with the provided information. The download uses the [@drms2019] package to obtain the images from the Joint Science Operations Center [@jsoc2022].

The SoFH also makes it possible to convert big datasets of FITS files to PNG only by selecting the images to convert. Moreover, it will automatically set up all other configurations regarding parameters to convert according to the imaging wavelength.

Besides using the software interface, more advanced users can run the download or conversion by command line.

> python main.py <flare_information.csv> <operation_number>

The <operation_number> is 1 for download or 2 for image conversion.

# References
