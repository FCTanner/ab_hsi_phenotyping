# ab_hyper_methods
Methods for processing of data acquired in automated high-throughput phenotyping system at 
[The Plant Accelerator®](https://plantphenomics.org.au/services/accelerator/)

## Description

Code and data underlying <mark>thesis chapter in:</mark>
## Getting started

### Contents

- Raw data
	* Raw RGB image data <mark>available via Pawsey</mark>
	* Raw hyperspectral data <mark>available via Pawsey</mark>
	* [Extracted trait data from LemnaTec system](https://github.com/FCTanner/ab_hsi_phenotyping/tree/main/raw_data/lemnatec)
	* [Visual scores](https://github.com/FCTanner/ab_hsi_phenotyping/tree/main/raw_data/scores)
	* [Average foreground reflectance](https://github.com/FCTanner/ab_hsi_phenotyping/tree/main/raw_data/hyperspectral)

- Processing methods
	* [Methods for calibration and segmentation of raw hyperspectral data](https://github.com/FCTanner/ab_hsi_phenotyping/tree/main/pre_processing/hyperspectral_segmentation)
	* [Hyperspectral data preprocessing](https://github.com/FCTanner/ab_hsi_phenotyping/tree/main/pre_processing/hyperspectral)
	* [Processing PSA](https://github.com/FCTanner/ab_hsi_phenotyping/tree/main/eda)

- Processed data
	* [Processed hyperspectral data](https://github.com/FCTanner/ab_hsi_phenotyping/tree/main/pre_processing/hyperspectral/out)
	* [Processed RGB data](https://github.com/FCTanner/ab_hsi_phenotyping/tree/main/eda/out/data)

- [PSA trait extraction](https://github.com/FCTanner/ab_hsi_phenotyping/tree/main/psa_analysis)

- [Methods for early detection of disease](https://github.com/FCTanner/ab_hsi_phenotyping/tree/main/detect_ab)

- [Methods for prediction of disease indices](https://github.com/FCTanner/ab_hsi_phenotyping/tree/main/predict_di)

- [EDA + score analysis](https://github.com/FCTanner/ab_hsi_phenotyping/tree/main/eda)

- [Visualization](https://github.com/FCTanner/ab_hsi_phenotyping/tree/main/visualize_spectrum)

### Data dictionary

#### [reflectance_2020.csv](https://github.com/FCTanner/ab_hsi_phenotyping/blob/main/raw_data/hyperspectral/reflectance_2020.csv)
#### [reflectance_2021.csv](https://github.com/FCTanner/ab_hsi_phenotyping/blob/main/raw_data/hyperspectral/reflectance_2022.csv)

| variable    | class     | description             |
|-------------|-----------|-------------------------|
| id_tag      | character | LemnaTec ID             |
| camera      | character | VNIR or SWIR camera     |
| date        | date      | Imaging date            |
| wavelength  | double    | Measured band [nm]      |
| reflectance | double    | Reflectance at the band |

#### [LemnaTec data 2020](https://github.com/FCTanner/ab_hsi_phenotyping/blob/main/raw_data/lemnatec/2020/0521_Chickpea%20Florian_rawdata%281%29_20200611.xlsx)
#### [LemnaTec data 2021](https://github.com/FCTanner/ab_hsi_phenotyping/blob/main/raw_data/lemnatec/2021/0588%20Chickpea%20Florian%20rawdata%281%29_20210623.xlsx)


| variable                      | class     | description          |
|-------------------------------|-----------|----------------------|
| Row No                        | double    | ID                   |
| Snapshot ID Tag               | character | LemnaTec ID          |
| Plant Species                 | character | Plant Species        |
| Genotype ID                   | character | Internal genotype ID |
| Treatment                     | character | Treatment            |
| Replicate                     | double    | Replicate            |
| Smarthouse                    | character | Greenhouse ID        |
| Lane                          | double    | Experimental design  |
| Position                      | double    | Experimental design  |
| Snapshot Time Stamp           | date      | Imaging time         |
| Time after Planting [d]       | double    | Days after planting  |
| Projected Shoot Area [pixels] | double    | Projected Shoot Area |
| …                             | …         | …                    |

#### [scores_2020.csv](https://github.com/FCTanner/ab_hsi_phenotyping/blob/main/raw_data/scores/scores_2020.csv)
#### [scores_2021.csv](https://github.com/FCTanner/ab_hsi_phenotyping/blob/main/raw_data/scores/scores_2021.csv)

| variable         | class     | description         |
|------------------|-----------|---------------------|
| id_with_controls | character | Genotype ID         |
| type             | character | Genotype group      |
| treatment        | character | Treatment           |
| id_tag           | character | LemnaTec ID         |
| di               | double    | Disease Index       |
| rep              | double    | Replicate           |
| lane             | double    | Experimental design |
| position         | double    | Experimental design |
| block            | double    | Experimental design |
| unit             | double    | Experimental design |


## Authors

Florian Tanner 

## Version history

## Licence

## Acknowledgements