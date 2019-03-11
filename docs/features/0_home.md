This is *continuous* version **c**.

To be updated regularly.

Viewable in [SHEBANQ]({{shebanq}}).

**the weekly updates have not started yet**.

## Introduction
This is the key to the meaning of the features of the
[BHSA dataset]({{repo}}).

We organize the features in several groups, roughly analogous to the
[types of objects](otype)
we have:

* [grid](#grid-features)
* [sectional](#sectional-features)
* [word](#word-features)
* [lexeme](#lexeme-features)
* [linguistic](#linguistic-features)
* [relationships](#relationships)
* [generic](#generic-features)

## Grid features

---|---|---
[otype](otype) | node type | `book` `verse` `clause` `phrase` `word`
[oslots](oslots) | slot containment | `1` `1-11` `2010-2015,2020-2030`
[otext](otext) | textapi | *no data, only specifications*  

## Sectional features

---|---|---
[book](book) | name of Bible book | `Genesis` `Psalmi` `Amos`
[chapter](chapter) | number of chapter within book | `3`
[verse](verse) | number of verse within chapter | `4`
[label](label#verse) | passage indicator | `AMOS 03,04`
[label](label#half-verse) | key for part within verse | `A` `B` `C`

## Lexeme features
(on node type `lex`)

---|---|---
[lex](lex) | lexeme consonantal transliterated | `>MR[`
[voc_lex](voc_lex) | lexeme pointed transliterated | `R;>CIJT`
[voc_lex_utf8](voc_lex_utf8) | lexeme pointed hebrew | `רֵאשִׁית`
[sp](sp) | part of speech | `verb` `subs`
[ls](ls) | lexical set | `quot` `ques`
[nametype](nametype) | type of named entity | `topo`
[gloss](gloss) | gloss | `beginning`
[language](language) | language (English name) | `Hebrew` `Aramaic`
[languageISO](languageISO) | language (ISO code) | `hbo` `arc`

## Word features

### Orthography

---|---|---|---|---
[g_cons](g_cons) | word | consonantal | transliterated | `>CR`
[g_cons_utf8](g_cons_utf8) | word | consonantal | hebrew | `אשׁר`
[g_word](g_word) | word | pointed | transliterated | `>:ACER&`
[g_word_utf8](g_word_utf8) | word | pointed | hebrew | `אֲשֶׁר`
[qere](qere) | word (qere) | consonantal | hebrew | `HAJ:Y;74>`
[qere_utf8](qere_utf8) | word (qere) | pointed | hebrew | `הַיְצֵ֣א`
[trailer_utf8](trailer_utf8) | after-word | pointed | hebrew | `׃ ׆̇`
[qere_trailer](qere_trailer) | after-word (qere) | pointed | hebrew | `׃ ׆̇`
[qere_trailer_utf8](trailer_utf8) | after-word (qere) | pointed | hebrew | `׃ ׆̇`

### Lexical (on node type `word`)

---|---|---|---|---
[lex](lex) | word | consonantal | transliterated | `>MR[`
[lex_utf8](lex_utf8) | word | consonantal | hebrew | `אמר`
[g_lex](g_lex) | word | pointed | transliterated | `>MER`
[g_lex_utf8](g_lex_utf8) | word | pointed | hebrew | `אמֶר`

---|---|---|---
[language](language) | language (English name) | `Hebrew` `Aramaic`
[languageISO](languageISO) | language (ISO code) | `hbo` `arc`
[sp](sp) | part of speech | `verb` `subs`
[pdp](pdp) | phrase dependent part of speech | `verb` `subs`
[ls](ls) | lexical set | `quot` `ques`

### Morphology

---|---|---
[gn](gn) [prs_gn](prs_gn) |  gender       | `m` `f`
[nu](nu) [prs_nu](prs_nu) |  number       | `sg` `pl` `du`
[ps](ps) [prs_ps](prs_ps) |  person       | `p1` `p2` `p3`
[st](st) | state | `a` `c` `e`
[vs](vs) | verbal stem | `qal` `piel` `nif` `hif`
[vt](vt) | verbal tense | `perf` `impf` `wayq`

### Morphemes

---|---|---|---|---
[nme](nme) | [g_nme](g_nme) | [g_nme_utf8](g_nme_utf8) | nominal ending | `/` `/IJM` `/@H`
[pfm](pfm) | [g_pfm](g_pfm) | [g_pfm_utf8](g_pfm_utf8) | preformative | `!!` `!J.I!` `!TI!`
[prs](prs) | [g_prs](g_prs) | [g_prs_utf8](g_prs_utf8) | pronominal suffix | `+OW` `+IJ` `+HEM`
[uvf](uvf) | [g_uvf](g_uvf) | [g_uvf_utf8](g_uvf_utf8) | univalent final | `~@H` `~IJ` `~OW`
[vbe](vbe) | [g_vbe](g_vbe) | [g_vbe_utf8](g_vbe_utf8) | verbal ending | `[` `[W.` `[T.IJ`
[vbs](vbs) | [g_vbs](g_vbs) | [g_vbs_utf8](g_vbs_utf8) | root formation | `]]` `]NI]` `]HA]`

### Statistics

---|---
[freq_lex](freq_lex) | frequency of lexeme
[freq_occ](freq_occ) | frequency of word occurrence
[rank_lex](rank_lex) | rank of lexeme
[rank_occ](rank_occ) | rank of word occurrence

## Linguistic features

### Sentence(-atom) features

Nothing specific, just a generic [number](number) feature.

### Clause(-atom) features

---|---|---
[typ](typ) | clause type | `AjCl` `WayX` `WXQt` `ZImX`
[kind](kind) | rough clause type | `VC` `NC` `WP`
[rela](rela) | clause constituent relation | `Adju` `Attr` `Coor`
[domain](domain) | text type ?? | `Q` `N` `D`
[txt](txt) | text type | `NQ` `NQQ` `QNQQ` `NQND`
[code](code) | clause atom relation | `200` `477` `999`
[is_root](is_root) | ??
[tab](tab) | hierarchical tabulation | `0` `3` `10` `29`
[pargr](pargr) | paragraph number | `1` `1.2` `2.3.4`
[instruction](instruction) | instruction | `.q` `.d` `..` `ve`

### Phrase(-atom) features

---|---|---
[typ](typ) | phrase type | `VP` `NP` `PP` `AdjP` `AdvP`
[rela](rela) | phrase atom relation | `Appo` `Para` `Resu`
[function](function) | phrase function | `Pred` `Subj`
[det](det) | determination | `det` `und`

## Relationships

---|---
[mother](mother) | relation of linguistic dependency
[distributional_parent](distributional_parent) | the parent in the distributional hierarchy (`-atoms`)
[functional_parent](functional_parent) | the parent in the distributional hierarchy (`sentence clause phrase`)

## Generic features

---|---|---
[number](number) | sequence number in context | `123`
[dist](dist) | distance to mother | `-10` `0`  `1` `8`
[dist_unit](dist_unit) | unit of measuring distance to mother | `clause_atoms` `phrase_atoms` `words`
[mother_object_type](mother_object_type) | object type of mother | `clause` `phrase` `subphrase` `word`
