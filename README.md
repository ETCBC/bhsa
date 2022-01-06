# Biblia Hebraica Stuttgartensia (Amstelodamensis)

[![SWH](https://archive.softwareheritage.org/badge/origin/https://github.com/ETCBC/bhsa/)](https://archive.softwareheritage.org/browse/origin/https://github.com/ETCBC/bhsa/)
[![DOI](https://zenodo.org/badge/104559294.svg)](https://zenodo.org/badge/latestdoi/104559294)
[![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)

[![etcbc](programs/images/etcbc.png)](http://www.etcbc.nl)
[![dans](programs/images/dans.png)](https://dans.knaw.nl/en)
[![tf](programs/images/tf-small.png)](https://annotation.github.io/text-fabric/tf)


### BHSA Family

* [bhsa](https://github.com/etcbc/bhsa) Core data and feature documentation
* [phono](https://github.com/etcbc/phono) Phonological representation of Hebrew words
* [parallels](https://github.com/etcbc/parallels) Links between similar verses
* [valence](https://github.com/etcbc/valence) Verbal valence for all occurrences
  of some verbs
* [trees](https://github.com/etcbc/trees) Tree structures for all sentences
* [bridging](https://github.com/etcbc/bridging) Open Scriptures morphology
  ported to the BHSA
* [pipeline](https://github.com/etcbc/pipeline) Generate the BHSA and SHEBANQ
  from internal ETCBC data files
* [shebanq](https://github.com/etcbc/shebanq) Engine of the
  [shebanq](https://shebanq.ancient-data.org) website

### Extended family

* [dss](https://github.com/etcbc/dss) Dead Sea Scrolls
* [extrabiblical](https://github.com/etcbc/extrabiblical)
  Extra-biblical writings from ETCBC-encoded texts
* [peshitta](https://github.com/etcbc/peshitta)
  Syriac translation of the Hebrew Bible
* [syrnt](https://github.com/etcbc/syrnt)
  Syriac translation of the New Testament

## About

This is the
[text-fabric](https://github.com/Dans-labs/text-fabric/wiki)
representation of the Hebrew Bible Database,
containing the text of the Hebrew Bible augmented with linguistic annotations compiled by the
[Eep Talstra Centre for Bible and Computer](http://etcbc.nl), VU University Amsterdam.

This repository contains several versions of the dataset, going back to 2011.
It is meant to accumulate new versions over the years.
The data in versions will not change, new versions will be stored next to the old versions.

So this repository addresses the need for permanency as well as the urge for change.

More information, especially about the data versions and annotation features, can be found on the
[data documentation pages](https://etcbc.github.io/bhsa/).

See also

* [Coding the Hebrew Bible](https://doi.org/10.1163/24523666-01000011)

## License

This work is licensed under a
[Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)](https://creativecommons.org/licenses/by-nc/4.0/).
That means:

* You may download the data and use it: process, copy, modify;
* You may use the data to create new software applications;
* You may use the data for research and publish any amount of results;
* When you publish this data or results you obtained from them, you have to comply with the following:
  * give proper attribution to the data when you use it in new applications,
    by citing this persistent identifier:
    [10.17026/dans-z6y-skyh](http://dx.doi.org/10.17026%2Fdans-z6y-skyh).
  * do not use the data for commercial applications without consent;
    for any commercial use, please contact the
    [German Bible Society](zentrale@dbg.de).

## How to use

This data can be processed by 
[Text-Fabric](https://annotation.github.io/text-fabric/tf).

Text-Fabric will automatically download the BHSA data.

After installing Text-Fabric, you can start the Text-Fabric browser by this command

```sh
text-fabric etcbc/bhsa
```

Alternatively, you can work in a Jupyter notebook and say

```python
from tf.app import use

A = use('etcbc/bhsa')
```

In both cases the data is downloaded and ends up in your home directory,
under `text-fabric-data`.

See also 
[start](https://nbviewer.jupyter.org/github/etcbc/bhsa/blob/master/tutorial/start.ipynb)
and
[search](https://nbviewer.jupyter.org/github/etcbc/bhsa/blob/master/tutorial/search.ipynb).

There is also a static search interface.
It is online, but it works on your computer, in the browser.

Just click
[bhsa-search](https://etcbc.github.io/bhsa-search/)
and off you go.

# Author

[Dirk Roorda](https://github.com/dirkroorda)

Note that the data content of this repo is the multi-year work of the 
[Eep Talstra Centre for Bible and Computer](http://etcbc.nl), VU University Amsterdam.
