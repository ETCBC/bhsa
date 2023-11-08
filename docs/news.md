# Updates

## 2021-11-30

It turned out that in version 2021

*   `gloss` was not present on word nodes
*   `lex0`, `lex_utf8` and `languageISO` were not present on lex nodes

Both have been remedied. Note that `g_lex` and `g_lex_utf8` are not defined on lex nodes,
because their values do not always agree between occurrences of the same lexeme. 

## 2021-08-24

Data version `2021` has arrived from the ETCBC. According to Constantijn Sikkel the most
consistent version ever.

## 2019-01-31

Some features only had values for lexeme nodes: `gloss nametype voc_lex voc_lex_utf8`.
If you want to know the values for individual words, you can easily go from a lexeme node
down to its occurrences with the `L.d()` function. That is, if you are programming.

But if you are querying, templates tend to become cumbersome because of this.
So I added the values of these features for lexemes to all of their occurrences.

## 2018-01-17

* There has been a conversion error: a single lexeme node became tied to a single stray node,
  due to a programming error.
  I have removed the error, and regenerated all versions of the BHSA, except 3, which was not affected.
* The feature `language` used to contain the values `Hebrew` and `Aramaic`, at least in SHEBANQ.
  But since we use the pipeline to generate data for SHEBANQ, the `language` feature contains the 
  ISO codes instead: `hbo` and `arc`.
  Because this breaks interoperability with Bible Online learner and Paratext
  I have decided to restore the feature `language` as it was before,
  and make a new feature `languageISO` with the ISO codes in it.

## 2017-10-13

There is a fixed version, 2017 (imported on 2017-10-06), and a nearly identical version `c`,
imported at the same time. 
Version `c` is continuous and will be frequently updated.
(Spoiler as of 2021-08-24: these updates have only happened a few times.
We discontinue continuous versions. All new versions will be stable versions.)

## 2017-10-05

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

Or see the complete [run]({{org}}/pipeline/blob/master/runs/2017-10-05.txt?raw=true).

## 2017-10-01

The ETCBC data source has moved.
It is now called 
**Biblia Hebraica Stuttgartensia (Amstelodamensis)**
(BHSA).

It resides in this repo, in several versions and formats.
This repo is involved in a
[pipeline]({{org}}/pipeline)
from the systems at the
ETCBC to GitHub repositories that host data in text-fabric format,
to the website SHEBANQ.

This repository only contains the core data of the ETCBC.

Additional data is still very much available, but has moved to
other repositories:

* [phono]({{org}}/phono)
* [parallels]({{org}}/parallels)
* [valence]({{org}}/valence)

This is by no means a closed set.
New research leads to new data, new repositories.
With a little extra effort, new repositories can be connected
to the pipeline.

## 2017-01-12

Added Strong numbers to Hebrew Data

## 2016-12-17

Added the *paragraph* features `pargr` and `instruction` to the `etcbc4c` dataset.
They were present in the `etcbc4b` version and on SHEBANQ, but I had left them out
for reasons of time pressure.
Now they are back in.

In order to use them, you have to update your data, which is as simple as

```sh
    cd ~/GitHub/text-fabric-data
    git pull origin master
```

## 2016-12-13

* Adapted the contents of the feature documentation to the new `etcbc4c` data.
* Added sidebar
* Better layout

## 2016-12-09

* Just started getting the Text-Fabric-Data documentation in place.
