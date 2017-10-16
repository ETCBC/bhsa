Clause atom relation ``code``
---------------------------------------------------------------
:doc:`frequency table of values <../index/code>`


This feature is present on objects of type *clause_atom*.

.. caution::
    This is a complex definition.
    The present text is derived from Constantijn's description of the
    QUEST II Database format.
    The definition needs review.

    See the hint at the end to see how you could use this feature.

Clause atom relation is denoted by a code of 1, 2, or 3 digits.

=================  ==========================================================
``0``              :ref:`No relation <norela>`
``10`` - ``16``    :ref:`Relative clause atoms <relative>`
``50`` – ``74``    :ref:`Infinitive construct clause atoms <infinitive>`
``100`` – ``167``  :ref:`Asyndetic clause atoms <asyndetic>`
``200`` - ``201``  :ref:`Parallel clause atoms <parallel>`
``220`` - ``223``  :ref:`Defective clause atoms <defective>`
``300`` - ``367``  :ref:`Conjunctive adverbs <cadverbs>`
``400`` - ``487``  :ref:`Coordinate clause atoms <coordinate>`
``500`` - ``567``  :ref:`Postulational clause atoms <postulational>`
``600`` - ``667``  :ref:`Conditional clause atoms <conditional>`
``700`` - ``767``  :ref:`Temporal clause atoms <temporal>`
``800`` - ``867``  :ref:`Final clause atoms <final>`
``900`` - ``967``  :ref:`Causal clause atoms <causal>`
``999``            :ref:`Direct speech <direct>`
=================  ==========================================================

These classes are of a distributional, not functional, nature.
They group lexemes which are hypothesised to share one or more functional aspects into tentative sets,
so that the resulting clause atom relations codes constitute a useful collection of data for further research.

See for example
Gino Kalkman's
`analysis of syntax in the poetry of the Psalms <https://shebanq.ancient-data.org/tools?goto=verbsystem>`_

.. caution::
    The notions distributional and functional should be explained somewhere, 
    on a separate page.
    The meaning of this sentence is difficult to follow.
    Which are the tentative sets of lexemes, which are the resulting clause atom relations?
    What is the useful collection of data?
    An example of research should be given or referred to.
    The reference to Gino's work could be more pin-pointed.

.. _norela:

``0`` No relation
^^^^^^^^^^^^^^^^^
The value ``0`` and a :doc:`dist <dist>` of 0 clause atoms to its mother mark a clause atom as the root of the tree of clause atom relations.

.. caution::
    Is the value of ``0`` sufficient?
    Can it occur that the value is ``0`` and the distance not?
    If not, the distance of 0 is not an extra condition, but an additional phenomenon.
    The definition should then say something like: (and in that case the :doc:`dist <dist>` is also ``0``).
    In order to understand this all, there should be an explanation of the intended model
    of clause atom relations. Is it a tree? How is it built up? Maybe a separate page.
    See also :doc:`tab <tab>`.

    Examples please.

.. _relative:

``10`` .. ``16`` Relative clause atoms
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Clause atoms whose opening phrase (first phrase?)
has :doc:`typ <typ>` ``CP`` (conjunctive phrase) and
:doc:`function <function>` ``Rela`` (relative).
The second digit denotes the tense of the verbal predicate of the daughter clause:

.. _tenses:

.. table:: Tenses

    ===== ===================== ====================
    ``0`` none
    ``1`` imperfect
    ``2`` perfect
    ``3`` imperative
    ``4`` infinitive construct
    ``5`` infinitive absolute
    ``6`` participle            (active and passive)
    ``7`` wayyiqtol
    ``8`` weyiqtol              !
    ===== ===================== ====================

.. caution::
    The ! appears where the QUEST documentation has a cross mark. 
    I do not know why these values have been marked.

.. _infinitive:

``50``– ``74``  Infinitive construct clause atoms
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Clause atoms of which the verbal predicate is an infinitive construct.
If you subtract 50, the remaining number denotes the class of the preposition used in the construction:

.. _prepositions:

.. table:: Preposition classes of the infinitive clause atom

    ====== ===========  =
    ``0``  none
    ``1``  >XR/
    ``2``  >L
    ``3``  >YL/         !
    ``4``  >T
    ``5``  B, BMW
    ``6``  BJN/         !
    ``7``  BL<DJ        !
    ``8``  *not used*
    ``9``  B<D/         !
    ``10`` ZWLH/        !
    ``11`` J<N/
    ``12`` K, KMW
    ``13`` *not used*
    ``14`` L, LMW
    ``15`` LM<N
    ``16`` *not used*
    ``17`` MN
    ``18`` *not used*
    ``19`` *not used*
    ``20`` <D
    ``21`` <L
    ``22`` <M
    ``23`` *not used*
    ``24`` TXT/
    ====== ===========  =

.. caution::
    The ! appears where the QUEST documentation has a cross mark. 
    I do not know why these values have been marked.

.. _asyndetic:

``100`` – ``167``  Asyndetic clause atoms
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Construction without a conjunction.
The second and third digit denote the tense of the verbal predicate of the daughter and
mother clause, respectively. See the :ref:`tense table <tenses>`.
See also :doc:`/texts/mother`.

.. _parallel:

``200`` - ``201``  Parallel clause atoms
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Two clause atoms are parallel if they concur in subject presence
and have equivalent phrases up to the predicate,
provided that the daughter is not subordinated.
See also :doc:`/texts/mother`.
If either predicate is absent,
the clause atoms must be of the same clause atom type (:doc:`typ <typ>`).


======= ================================================================================
``200`` Identical clause atom opening.
``201`` Identical clause atom opening when disregarding the coordinating conjunction(s).
======= ================================================================================

.. _defective:

``220`` - ``223``  Defective clause atoms
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
A clause atom is defective if there is another clause atom which contains
the predicate (or the main part) of the clause.

======= ==========================================
``220`` No verbal predicate in mother or daughter
``221`` Unclassified clause atom relation
``222`` Verbal predicate in daughter clause atom
``223`` Verbal predicate in mother clause atom.
======= ==========================================

See also :doc:`/texts/mother`.

.. _cadverbs:

``300`` - ``367``  Conjunctive adverbs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Asyndetic construction, but with a conjunctive adverb.
The second and third digit denote the tense of the verbal predicate of the daughter and
mother clause, respectively. See the :ref:`tense table <tenses>`.
See also :doc:`/texts/mother`.

.. _coordinate:

``400`` - ``487``  Coordinate clause atoms
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Construction with a conjunction from class 400, the *coordinating* conjunctions:
The second and third digit denote the tense of the verbal predicate of the daughter and
mother clause, respectively. See the :ref:`tense table <tenses>`.
See also :doc:`/texts/mother`.

.. _conjunctionsopen:

.. table:: Conjunction classes of clause atom opening

    ======= ============= ========================
    ``400`` coordinating  >W, W
    ``500`` postulational >CR, DJ, H, ZW, KJ, C
    ``600`` conditional   >LW, >M, HN, LHN=, LW, LWL>
    ``800`` final         PN
    ======= ============= ========================

The conjunction class is determined by the conjunction opening conjunction phrase.

.. caution::
    Too terse:
    "the conjunction opening conjunction phrase".
    Expand or give an example.

    code 800 also occurs in the table of
    :ref:`Preposition classes of clause atom opening <prepositionsopen>`

.. _postulational:

``500`` - ``567``  Postulational clause atoms
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Construction with a conjunction from class 500, the *postulational* conjunctions:
The second and third digit denote the tense of the verbal predicate of the daughter and
mother clause, respectively. See the :ref:`tense table <tenses>`.
See also :doc:`/texts/mother`.

.. _conditional:

``600`` - ``667``  Conditional clause atoms
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Construction with a conjunction from class 600, the *conditional* conjunctions:
The second and third digit denote the tense of the verbal predicate of the daughter and
mother clause, respectively. See the :ref:`tense table <tenses>`.
See also :doc:`/texts/mother`.

.. _temporal:

``700`` - ``767``  Temporal clause atoms
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Construction with a conjunction from class 700, the *conditional* conjunctions:
The second and third digit denote the tense of the verbal predicate of the daughter and
mother clause, respectively. See the :ref:`tense table <tenses>`.
See also :doc:`/texts/mother`.

.. _prepositionsopen:

.. table:: Preposition classes of clause atom opening

    ======= ==========================================
    ``700`` >XR/, >L, B, BMW, VRM/, K, KMW, L, LMW, <D
    ``800`` BLT/, ZWLH/, LM<N, MN
    ``900`` J<N/, <L, <QB/
    ======= ==========================================

This preposition class is determined by the preposition that heads the clause opening conjunction phrase.

.. caution::
    Too terse:
    "that heads the clause opening conjunction phrase".
    Expand or give an example.

    code 800 also occurs in the table of
    :ref:`Conjunction classes of clause atom opening <conjunctionsopen>`

.. _final:

``800`` - ``867``  Final clause atoms
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Construction with a conjunction from class 800, the *final* conjunctions:
The second and third digit denote the tense of the verbal predicate of the daughter and
mother clause, respectively. See the :ref:`tense table <tenses>`.
See also :doc:`/texts/mother`.

.. _causal:

``900`` - ``967``  Causal clause atoms
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Construction with a conjunction from class 900, the *causal* conjunctions:
The second and third digit denote the tense of the verbal predicate of the daughter and
mother clause, respectively. See the :ref:`tense table <tenses>`.
See also :doc:`/texts/mother`.

.. _direct:

``999`` Direct speech
^^^^^^^^^^^^^^^^^^^^^
The clause atom in question starts a direct speech section.

A section of direct speech is usually introduced by a clause atom
with a verbum dicendi. In this case, the direct speech section
depends on the introductory clause atom in terms of clause atom
relations. The daughter clause atom (the main clause atom of the
direct speech section) carries the :doc:`instruction <instruction>`
'q' and has a
relation 999 with its mother, the introductory clause atom.

But there are other cases, in which the the direct speech section
is not introduced at all (Jes 14:16) or in which it is declared by
an embedded clause atom (Mal 3:17). In such cases, the main clause
atom of the direct speech section still carries the :doc:`instruction <instruction>`
'q', but no longer has a relation 999 with its mother. If there is
a declarative clause atom, it will have a relation 999 with _its_
mother, which is not necessarily the main clause atom of the direct
speech section, as an example like Mal 3:17 shows.

In all cases, the :doc:`instruction <instruction>` 'q' means the start of a clause atom
hierarchy of direct speech. In view of the above, however, we can
no longer maintain a direct coupling between 'q' and relation 999.
We propose to extend the interpretation of relation 999 as follows.
The meaning of relation 999 is that of a declaration of direct
speech. Either before the facts, if the daughter starts the direct
speech, or after the facts, if the daughter has the verbum dicendi.
In case of the latter, the daughter carries the :doc:`instruction <instruction>` '#' for
a new embedded paragraph, but pops the Q from the Text Type.
See also :doc:`/texts/mother`.

.. caution::
    Is the "daughter" clause the object in question?

    What if a direct speech clause also fits the pattern of one of the other cases?

.. hint::
    Here is a public MQL query by Martijn Naaijer that detects chunks of direct speech.
    It uses the combined information carried by the ``code`` feature and the 
    :doc:`txt <txt>` feature. View the query on
    `SHEBANQ <http://shebanq.ancient-data.org/hebrew/query?id=518>`_.
