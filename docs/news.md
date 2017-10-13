---
title: News
type: pages
---

### 2017-10-13

There is a fixed version, 2017 (imported on 2017-10-06), and a nearly identical version `c`,
imported at the same time. 
Version `c` is continuous and will be frequently updated.

### 2017-10-05

* An old version, `3` from 2011 has been added.
  This is an interesting version, because it shows the evolution of the database and the
  encoding of linguistics in features.
  It was also a nice test for the pipeline from ETCBC data to the TF repos.
  A bit more sophistication was needed in the MQL conversion, and some feature names needed to
  be passed as a parameter, instead of being hard-coded, but that was basically it.
* All generated TF files now mention in their metadata the name and version of the core BHSA set
  they depend upon. All TF data in the core database and related repositories has been regenerated
  in one single run of the pipeline, which took 59 minutes to complete. Here are the last lines
  of the scroll of progress messages:

```
----------------------------------------------------------------------------------------------
-     58m 41s SUCCES [parallels/parallels]                                                   -
----------------------------------------------------------------------------------------------


**********************************************************************************************
*                                                                                            *
*     58m 41s SUCCES [parallels]                                                             *
*                                                                                            *
**********************************************************************************************


##############################################################################################
#                                                                                            #
#     58m 41s SUCCES [c]                                                                     #
#                                                                                            #
##############################################################################################
```

Or see the complete [run](https://github.com/ETCBC/pipeline/blob/master/runs/2017-10-05.txt?raw=true).

### 2017-10-01

The ETCBC data source has moved.
It is now called 
**Biblia Hebraica Stuttgartensia (Amstelodamensis)**
(BHSA).

It resides in this repo, in several versions and formats.
This repo is involved in a
[pipeline](https://github.com/ETCBC/pipeline)
from the systems at the
ETCBC to github repositories that host data in text-fabric format,
to the website SHEBANQ.

This repository only contains the core data of the ETCBC.

Additional data is still very much available, but has moved to
other repositories:

* [phono](https://github.com/ETCBC/phono)
* [parallels](https://github.com/ETCBC/parallels)
* [valence](https://github.com/ETCBC/valence)

This is by no means a closed set.
New research leads to new data, new repositories.
With a little extra effort, new repositories can be connected
to the pipeline.

### 2017-01-12

Added Strong numbers to Hebrew Data

### 2016-12-17

Added the *paragraph* features `pargr` and `instruction` to the etcbc 4c dataset.
They were present in the etcbc4b version and on SHEBANQ, but I had left them out
for reasons of time pressure.
Now they are back in.

In order to use them, you have to update your data, which is as simple as

```sh
    cd ~/github/text-fabric-data
    git pull origin master
```

### 2016-12-13

* Adapted the contents of the feature documentation to the new etcbc 4c data.
* Added sidebar
* Better layout

### 2016-12-09

* Just started getting the Text-Fabric-Data documentation in place.
