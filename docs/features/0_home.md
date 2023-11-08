This is data version **2021**,
viewable in [SHEBANQ]({{shebanq}}).

## Introduction
This is the key to the meaning of the features of the
[BHSA dataset]({{repo}}).

We organize the features in several groups, roughly analogous to the
[types of objects](otype.md)
we have:

* [grid](#grid-features)
* [sectional](#sectional-features)
* [word](#word-features)
* [lexeme](#lexeme-features)
* [linguistic](#linguistic-features)
* [relationships](#relationships)
* [generic](#generic-features)

## Grid features

name|description|examples
---|---|---
[`otype`](otype.md) | node type | `book` `verse` `clause` `phrase` `word`
[`oslots`](oslots.md) | slot containment | `1` `1-11` `2010-2015,2020-2030`
[`otext`](otext.md) | text API | *no data, only specifications*  

## Sectional features

name|description|examples
---|---|---
[`book`](book.md) | name of Bible book | `Genesis` `Psalmi` `Amos`
[`chapter`](chapter.md) | number of chapter within book | `3`
[`verse`](verse.md) | number of verse within chapter | `4`
[`label`](label#verse) | passage indicator | `AMOS 03,04`
[`label`](label#half-verse) | key for part within verse | `A` `B` `C`

## Lexeme features
(on node type `lex`)

name|description|examples
---|---|---
[`lex`](lex.md) | lexeme consonantal transliterated | `>MR[`
[`voc_lex`](voc_lex.md) | lexeme pointed transliterated | `R;>CIJT`
[`voc_lex_utf8`](voc_lex_utf8.md) | lexeme pointed hebrew | `רֵאשִׁית`
[`sp`](sp.md) | part of speech | `verb` `subs`
[`ls`](ls.md) | lexical set | `quot` `ques`
[`nametype`](nametype.md) | type of named entity | `topo`
[`gloss`](gloss.md) | gloss | `beginning`
[`language`](language.md) | language (English name) | `Hebrew` `Aramaic`
[`languageISO`](languageISO.md) | language (ISO code) | `hbo` `arc`

## Word features

### Orthography

name|node type|description|mode|examples
---|---|---|---|---
[`g_cons`](g_cons.md) | word | consonantal | transliterated | `>CR`
[`g_cons_utf8`](g_cons_utf8.md) | word | consonantal | hebrew | `אשׁר`
[`g_word`](g_word.md) | word | pointed | transliterated | `>:ACER&`
[`g_word_utf8`](g_word_utf8.md) | word | pointed | hebrew | `אֲשֶׁר`
[`qere`](qere.md) | word (qere) | consonantal | hebrew | `HAJ:Y;74>`
[`qere_utf8`](qere_utf8.md) | word (qere) | pointed | hebrew | `הַיְצֵ֣א`
[`trailer_utf8`](trailer_utf8.md) | after-word | pointed | hebrew | `׃ ׆̇`
[`qere_trailer`](qere_trailer.md) | after-word (qere) | pointed | hebrew | `׃ ׆̇`
[`qere_trailer_utf8`](trailer_utf8.md) | after-word (qere) | pointed | hebrew | `׃ ׆̇`

### Lexical (on node type `word`)

name|node type|description|mode|examples
---|---|---|---|---
[`lex`](lex.md) | word | consonantal | transliterated | `>MR[`
[`lex_utf8`](lex_utf8.md) | word | consonantal | hebrew | `אמר`
[`g_lex`](g_lex.md) | word | pointed | transliterated | `>MER`
[`g_lex_utf8`](g_lex_utf8.md) | word | pointed | hebrew | `אמֶר`

name|description|examples
---|---|---
[`language`](language.md) | language (English name) | `Hebrew` `Aramaic`
[`languageISO`](languageISO.md) | language (ISO code) | `hbo` `arc`
[`sp`](sp.md) | part of speech | `verb` `subs`
[`pdp`](pdp.md) | phrase dependent part of speech | `verb` `subs`
[`ls`](ls.md) | lexical set | `quot` `ques`

### Morphology

name|description|examples
---|---|---
[`gn`](gn.md) [`prs_gn`](prs_gn.md) |  gender       | `m` `f`
[`nu`](nu.md) [`prs_nu`](prs_nu.md) |  number       | `sg` `pl` `du`
[`ps`](ps.md) [`prs_ps`](prs_ps.md) |  person       | `p1` `p2` `p3`
[`st`](st.md) | state | `a` `c` `e`
[`vs`](vs.md) | verbal stem | `qal` `piel` `nif` `hif`
[`vt`](vt.md) | verbal tense | `perf` `impf` `wayq`

### Morphemes

name (consonantal transliterated)|name (pointed transliterated)|name (pointed hebrew)|description|examples
---|---|---|---|---
[`nme`](nme.md) | [`g_nme`](g_nme.md) | [`g_nme_utf8`](g_nme_utf8.md) | nominal ending | `/` `/IJM` `/@H`
[`pfm`](pfm.md) | [`g_pfm`](g_pfm.md) | [`g_pfm_utf8`](g_pfm_utf8.md) | preformative | `!!` `!J.I!` `!TI!`
[`prs`](prs.md) | [`g_prs`](g_prs.md) | [`g_prs_utf8`](g_prs_utf8.md) | pronominal suffix | `+OW` `+IJ` `+HEM`
[`uvf`](uvf.md) | [`g_uvf`](g_uvf.md) | [`g_uvf_utf8`](g_uvf_utf8.md) | univalent final | `~@H` `~IJ` `~OW`
[`vbe`](vbe.md) | [`g_vbe`](g_vbe.md) | [`g_vbe_utf8`](g_vbe_utf8.md) | verbal ending | `[` `[W.` `[T.IJ`
[`vbs`](vbs.md) | [`g_vbs`](g_vbs.md) | [`g_vbs_utf8`](g_vbs_utf8.md) | root formation | `]]` `]NI]` `]HA]`

### Statistics

name|description
---|---
[`freq_lex`](freq_lex.md) | frequency of lexeme
[`freq_occ`](freq_occ.md) | frequency of word occurrence
[`rank_lex`](rank_lex.md) | rank of lexeme
[`rank_occ`](rank_occ.md) | rank of word occurrence

## Linguistic features

### Sentence(-atom) features

Nothing specific, just a generic [`number`](number.md) feature.

### Clause(-atom) features

name|description|examples
---|---|---
[`typ`](typ.md) | clause type | `AjCl` `WayX` `WXQt` `ZImX`
[`kind`](kind.md) | rough clause type | `VC` `NC` `WP`
[`rela`](rela.md) | clause constituent relation | `Adju` `Attr` `Coor`
[`domain`](domain.md) | text type ?? | `Q` `N` `D`
[`txt`](txt.md) | text type | `NQ` `NQQ` `QNQQ` `NQND`
[`code`](code.md) | clause atom relation | `200` `477` `999`
[`is_root`](is_root.md) | ??
[`tab`](tab.md) | hierarchical tabulation | `0` `3` `10` `29`
[`pargr`](pargr.md) | paragraph number | `1` `1.2` `2.3.4`
[`instruction`](instruction.md) | instruction | `.q` `.d` `..` `ve`

### Phrase(-atom) features

name|description|examples
---|---|---
[`typ`](typ.md) | phrase type | `VP` `NP` `PP` `AdjP` `AdvP`
[`rela`](rela.md) | phrase atom relation | `Appo` `Para` `Resu`
[`function`](function.md) | phrase function | `Pred` `Subj`
[`det`](det.md) | determination | `det` `und`

## Relationships

name|description
---|---
[`mother`](mother.md) | relation of linguistic dependency
[`distributional_parent`](distributional_parent.md) | the parent in the distributional hierarchy (`-atoms`)
[`functional_parent`](functional_parent.md) | the parent in the distributional hierarchy (`sentence clause phrase`)

## Generic features

name|description|examples
---|---|---
[`number`](number.md) | sequence number in context | `123`
[`dist`](dist.md) | distance to mother | `-10` `0`  `1` `8`
[`dist_unit`](dist_unit.md) | unit of measuring distance to mother | `clause_atoms` `phrase_atoms` `words`
[`mother_object_type`](mother_object_type.md) | object type of mother | `clause` `phrase` `subphrase` `word`
