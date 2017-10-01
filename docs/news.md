---
title: News
type: pages
---

### 2017-01-10

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

Added the *paragraph* features `pargr` and `instruction` to the etcbc4c dataset.
They were present in the etcbc4b version and on SHEBANQ, but I had left them out
for reasons of time pressure.
Now they are back in.

In order to use them, you have to update your data, which is as simple as

```sh
    cd ~/github/text-fabric-data
    git pull origin master
```

### 2016-12-13

* Adapted the contents of the feature documentation to the new etcbc4c data.
* Added sidebar
* Better layout

### 2016-12-09

* Just started getting the Text-Fabric-Data documentation in place.
