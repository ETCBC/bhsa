# Words and morphemes

Words may consist of parts that carry parts of the meaning. These parts are called morphemes.
They can be verbal and nominal endings, which signal grammatical functions such as person, number, gender, state, tense, mood.
They can also be pronominal suffixes, which are almost separate lexemes.

The BHSA dataset distinguishes the following morphological elements in a word:

* prefix - lexeme - suffix - enclitic

* vowel-pattern

The information in each of these elements is carried by one or more features in the BHSA dataset.
These features are also represented by a single shortcut character, which shows up in some feature values, which is why we mention them here.

## prefix

feature|code|description
---|---|---
[pfm](features/pfm.md) | `!` | preformative
[vbs](features/vbs.md) | `]` | verbal stem (root formation)

## lexeme

feature|description
---|---
[lex](features/lex.md) |             word (as dictionary entry)
[g_word](features/g_word.md) |       word (as occurrence in the text)

## suffix

feature|code|description
---|---|---
[vbe](features/vbe.md) | `[` | verbal ending
[nme](features/nme.md) | `/` | nominal ending
[uvf](features/uvf.md) | `~` | univalent final

## enclitic

feature|code|description
---|---|---
[prs](features/prs.md) | `+` | pronominal suffix

## vowel pattern
Not present as a separate feature in the dataset.

All these features encode the information that is encountered in the text.
So, although the values carry grammatical information, these features do not label the grammatical information. 

There is, however, one level of abstraction: 
the morpheme occurrences as they occur in the text, also called the *graphical forms*,
are grouped around abstract, *paradigmatical* forms. 
The *paradigmatical* forms come close to specifying grammatical information,
but usually they do not do that on their own,
but the information of several paradigmatical forms must be combined
to arrive at a definite grammatical label, if this is possible at all.

If you need to now the grammatical label assigned to a word, e.g. *gender* = `f`,
or *state* = `a`, you need to use other features:

features|description|examples
---|---|---
[gn](features/gn.md) [prs_gn](features/prs_gn.md) |  gender       | `m` `f`
[nu](features/nu.md) [prs_nu](features/prs_nu.md) |  number       | `sg` `pl` `du`
[ps](features/ps.md) [prs_ps](features/prs_ps.md) |  person       | `p1` `p2` `p3`
[st](features/st.md) |  state        | `a` `c` `e`
[vs](features/vs.md) |  verbal stem  | `qal` `piel` `nif` `hif`
[vt](features/vt.md) |  verbal tense | `perf` `impf` `wayq`
