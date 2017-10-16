Name type ``nametype``
----------------------------------------------------------------

The type of a named entity.

This feature is present on objects of type *word*.

It is a comma separated list of the following values:

=========== =======================================
``pers``    person
``mens``    measurement unit
``gens``    people
``topo``    place
``ppde``    demonstrative personal pronoun
=========== =======================================

This feature has been added to the database in a later stage as package called ``lexicon``.

You can use it in SHEBANQ queries.

If you want to use it in LAF-Fabric, you have to load ``lexicon`` as *annox*.
Consult the `LAF-Fabric API reference on annoxes <http://laf-fabric.readthedocs.io/en/latest/texts/API-reference.html#extra-annotation-packages>`_.

