# Solar Flares Hunter -- SoFH
## A python software to download solar images and convert from fits to png files.
The main goal of SoFH software is to facilitate and accelerate the process of downloading solar images in the most common wavelengths: HMI Continuum, HMI Magnetograms, AIA1600, and AIA1700. For that task, the user needs to inform the parameters about the wanted image in a CSV file. The necessary parameters are date, time and type of solar flare. The software will download and save the images in different folders with the provided information. The download uses the drms package to obtain the images from the Joint Science Operations Center.

The SoFH also makes it possible to convert big datasets of FITS files to PNG only by selecting the images to convert. Moreover, it will automatically set up all other configurations regarding parameters to convert according to the imaging wavelength.

Also, it is mandatory to register an e-mail on JSOC (on [this](http://jsoc.stanford.edu/ajax/register_email.html) page), to allow to export files.
All packages needed to run the software are in "requirements.txt" file, which can be used to run the virtual environment to allow using the software. All commands needed to run the code are listed bellow. 

## Um software em python para download de imagens solares e conversão de arquivos fits para png.
O principal objetivo do SoFH é facilitar e acelerar o processo de download de imagens do Sol nos comprimentos de onda: HMI Continuum, HMI Magnetogramas, AIA1600 e AIA1700. Para isso, o usuário deve fornecer parâmetros sobre a explosão espacial desejada em um arquivo CSV. É necessário fornecer data, hora e tipo da explosão solar. O software irá salvar as imagens em diferentes pastas de acordo com as informações fornecidas. O download utiliza o pacote drms para obter as imagens do Joint Science Operations Center..

O software também torna possível a conversão de grandes datasets de arquivos FITS para PNG, apenas selecionando as imagens para converter.

Além disso, é obrigatório possuir um e-mail cadastrado junto ao JSOC (através do [link](http://jsoc.stanford.edu/ajax/register_email.html)) para permitir exportar os arquivos.
Todas as bibliotecas necessárias para utilziar o software estão no arquivo "requirements.txt", o qual pode ser usado para instalar o ambiente virtual e utilizar o software. As instruções de ambiente e para utilizar o software encontram-se abaixo.
### Setup Environment / Preparando o ambiente
> pip install virtualenv

> virtualenv venv

> pip install -r requirements.txt

## Syntax / Sintaxe
> python src\main.py

### Usefull links / Links úteis

Guide to SDO Data Analysis - Click [here](https://www.lmsal.com/sdodocs/doc/dcur/SDOD0060.zip/zip/entry/)

Tutorial DRMS Package - Click [here](https://docs.sunpy.org/projects/drms/en/latest/tutorial.html)  

Joint Science Operations Center (JSOC) - Click [here](http://jsoc.stanford.edu)
