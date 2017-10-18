---
title: Features
feat: false
---

This is *frozen* version **3**, taken from ETCBC on 2011-12-31.

This version has been deposited in the DANS-EASY archive by Eep Talstra in person,
during the Lorentz conference
[Biblical Scholarship and Humanities Computing: Data Types, Text, Language and Interpretation]({{site.lorentz}}), 2012-02-10 and can be retrieved as an MQL dump from
[DOI: {{site.doi3}}]({{site.doi3_url}}).

The data has been re-archived in Zenodo: [DOI: {{site.doiBhsa}}]({{site.doiBhsa_url}}).

Not viewable in [SHEBANQ]({{site.shebanq}}).

This data has not been enriched with extra ETCBC data, nor with a phonetic transcription.
But statistical features have been added.

# Feature documentation
The features of this version are not documented,
but the table below maps them to `2016` features.
There is no exact one-one correspondence, and even when features
are neatly mapped, they may differ in structure and nature of their values.

You have the power of text-fabric at your disposal to explore the differences in greater detail.

version `3` | version `2016` | example values | comments
---|---
`aramaic_definite_article`                     | X                        | `Absent` `>`           |
`clause_atom_number`                           | [number](../2016/number) |                        |
`clause_atom_relation`                         | [code](../2016/code)     |                        |
`clause_atom_relation_daughter_tense`          | X                        | `unknown`              | garbage feature
`clause_atom_relation_kind`                    | X                        | `No_relation`          | garbage feature
`clause_atom_relation_mother_tense`            | X                        | `unknown`              | garbage feature
`clause_atom_relation_preposition_class`       | X                        | `none`                 | garbage feature
`clause_atom_type`                             | [typ](../2016/typ)       |                        |
`clause_constituent_relation`                  | [rela](../2016/rela)     |                        |
`clause_type`                                  | [typ](../2016/typ)       |                        |
`determination`                                | [det](../2016/det)       |                        |
`domain`                                       | [domain](../2016/domain) |                        |
`embedding_domain`                             | X                        |                        | related to `domain`
`gender`                                       | [gn](../2016/gn)         |                        |
`graphical_aramaic_definite_article`           | X                        | `א֒` `ה֙` `י`            |
`graphical_aramaic_definite_article_plain`     | X                        | `א־` `ה` `י`           |
`graphical_locative`                           | [g_uvf_utf8](../2016/g_uvf_utf8) |  `ָה֒` `ָה׀`      | but `uvf` is richer
`graphical_locative_plain`                     | [g_uvf](../2016/g_uvf)   | `ה` `ה־`               | but `uvf` is richer
`graphical_nominal_ending`                     | [g_nme_utf8](../2016/g_nme_utf8) |                |
`graphical_nominal_ending_plain`               | [g_nme](../2016/g_nme)   |                        |
`graphical_preformative`                       | [g_pfm_utf8](../2016/g_pfm_utf8) |                |
`graphical_preformative_plain`                 | [g_pfm](../2016/g_pfm)   |                        |
`graphical_pron_suffix`                        | [g_prs_utf8](../2016/g_prs_utf8) |                |
`graphical_pron_suffix_plain`                  | [g_prs](../2016/g_prs)   |                        |
`graphical_root_formation`                     | [g_vbs_utf8](../2016/g_vbs_utf8) |                | considerable differences in values
`graphical_root_formation_plain`               | [g_vbs](../2016/g_vbs)   |                        | considerable differences in values
`graphical_verbal_ending`                      | [g_vbe_utf8](../2016/g_vbe_utf8) |                |
`graphical_verbal_ending_plain`                | [g_vbe](../2016/g_vbe)   |                        |
`half_verse`                                   | [label](../2016/label)   |                        |
`indentation`                                  | [tab](../2016/tab)       |                        |
`is_apposition`                                | X                        | `false`                | garbage feature
`language`                                     | [language](../2016/language) |                    |
`levels_of_embedding`                          | X                        | `0` ... `6`            |
`lexical_set`                                  | [ls](../2016/ls)         |                        |
`locative`                                     | [uvf](../2016/uvf)       |                        | but `uvf` is richer
`mother`                                       | [mother](../2016/mother) |                        |
`noun_type`                                    | [sp](../2016/sp)         |                        | but `sp` is richer
`number`                                       | [number](../2016/number) |                        |
`number_within_chapter`                        | [number](../2016/number) |                        |
`number_within_clause`                         | [number](../2016/number) |                        |
`number_within_sentence`                       | [number](../2016/number) |                        |
`old_lexeme`                                   | X                        |                        |
`old_lexeme_utf8`                              | X                        |                        |
`paradigmatic_nominal_ending`                  | [nme](../2016/nme)       |                        |
`paradigmatic_preformative`                    | [pfm](../2016/pfm)       |                        |
`paradigmatic_pron_suffix`                     | [prs](../2016/prs)       |                        |
`paradigmatic_root_formation`                  | [vbs](../2016/vbs)       |                        |
`paradigmatic_verbal_ending`                   | [vbe](../2016/vbe)       |                        |
`parents`                                      | [functional_parent](../2016/functional_parent) and [distributional_parent](../2016/distributional_parent) | |
`part_of_speech`                               | [sp](../2016/sp)         |                        |
`person`                                       | [ps](../2016/ps)         |                        |
`phrase_atom_number`                           | [number](../2016/number) |                        |
`phrase_atom_relation`                         | [rela](../2016/rela)     | `Appo` `Link` `Para` `Spec` |
`phrase_atom_type`                             | [type](../2016/type)     | `VP` `NP` `PP`         |
`phrase_dependent_part_of_speech`              | [pdp](../2016/pdp)       |                        |
`phrase_function`                              | [function](../2016/function) |                    |
`phrase_type`                                  | [type](../2016/type)     |                        |
`pronoun_type`                                 | [sp](../2016/sp)         |                        |
`sentence_atom_number`                         | [number](../2016/number) |                        |
`state`                                        | [st](../2016/st)         |                        |
`stem`                                         | [vs](../2016/vs)         |                        |
`subphrase_kind`                               | X                        | `daughter` `mother`    |
`subphrase_type`                               | [typ](../2016/typ)       |                        |
`suffix_gender`                                | [prs_gn](../2016/prs_gn) |                        |
`suffix_number`                                | [prs_nu](../2016/prs_nu) |                        |
`suffix_person`                                | [prs_ps](../2016/prs_ps) |                        |
`tense`                                        | [vt](../2016/vt)         |                        |
`text_plain`                                   | [g_cons_utf8](../2016/g_cons_utf8) |              |
`text_type`                                    | [txt](../2016/txt)       |                        |
`verse_label`                                  | [label](../2016/label)   |                        |
`vocalized_lexeme`                             | [voc_lex](../2016/voc_lex) |                      |
`vocalized_lexeme_utf8`                        | [voc_lex_utf8](../2016/voc_lex_utf8) |            |
`word_number_within_book`                      | [number](../2016/number) |                        |
