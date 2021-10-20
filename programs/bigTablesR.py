# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.11.4
#   kernelspec:
#     display_name: R
#     language: R
#     name: ir
# ---

# <img align="right" src="images/dans-small.png"/>
# <img align="right" src="images/tf-small.png"/>
# <img align="right" src="images/etcbc.png"/>
#
#
# # Import BHSA data into R
#
# This notebook contains the R instructions to load the
# [bigTables](bigTables.ipynb) export of the BHSA
# and save it in the much more compact `.rds` format.
#
# We then perform some simple information extracting on the data.
# For comparison, the same information extraction has been done for Pandas:
# in [bigTablesP](bigTablesP.ipynb).
#
# Note that we have to ignore quotes and comment signs!
#
# First we load the big text file with all information. This will take 3 minutes or so.

bhsa = read.table(
    '../_temp/2017/r/bhsa2017.txt',
    sep="\t",
    header=TRUE,
    comment.char="",
    quote="",
    as.is = TRUE,
)
dim(bhsa)

# Now we save it into compact `.rds` format.

saveRDS(
    object=bhsa,
    file='../_temp/2017/r/bhsa2017.rds'
)

# We load the data again, now from the compact representation. Much quicker. Still 40 seconds.

bhsa = readRDS(
    file='../_temp/2017/r/bhsa2017.rds'
)

dim(bhsa)

head(bhsa, n=30)

# # Books
#
# Let us extract some data.
# First a list of the book names.

books = bhsa$book[bhsa$otype == 'book']
paste(books, collapse=' ')

# # Text
#
# Now the complete text of the whole bible.

words = which(bhsa$otype == 'word')
text = paste(
    bhsa$g_word_utf8[words], sub('׃', '׃\n', bhsa$trailer_utf8[words]),
    sep='', collapse=''
)
write(text, file='../_temp/2017/r/plainTextFromR.txt')

# # Drill down to a passage
#
# Let us get the part of speech of the words from the first verse:

wordIds = bhsa$n[bhsa$otype=='word' & bhsa$in.verse==1414190]
wordIds

# Now the *text* of the first verse.

words = which(bhsa$n %in% wordIds)
gsub('׃', '׃\n',
    paste(bhsa$g_word_utf8[words], bhsa$trailer_utf8[words], collapse='')
)

# Let us get the words and text of an arbitrary passage, say Psalmi 131:2

verseId = bhsa$n[bhsa$otype == 'verse' & bhsa$book == 'Psalmi' & bhsa$chapter == 131 & bhsa$verse == 2]
verseId
wordIds = bhsa$n[bhsa$otype=='word' & bhsa$in.verse == verseId]
wordIds
words = which(bhsa$n %in% wordIds)
gsub('׃', '׃\n',
    paste(bhsa$g_word_utf8[words], bhsa$trailer_utf8[words], collapse='')
)

# Now let us organize this in two functions: one that returns the verse object given a passage, and one that prints the texts of the words in a given object.

# +
object2text = function(n) {
    otype = bhsa$otype[bhsa$n == n]
    wordIds = eval(parse(text=paste("bhsa$n[bhsa$otype=='word' & bhsa$in.", otype, '==n]', sep='')))
    words = which(bhsa$n %in% wordIds)
    return(gsub('׃', '׃\n',
        paste(bhsa$g_word_utf8[words], bhsa$trailer_utf8[words], collapse='')
    ))
}

verse2object = function(book, chapter, verse) {
    return(bhsa$n[bhsa$otype == 'verse' & bhsa$book == book & bhsa$chapter == chapter & bhsa$verse == verse])
}
verse2text = function(book, chapter, verse) {
    return(object2text(verse2object(book, chapter, verse)))
}
chapter2object = function(book, chapter) {
    return(bhsa$n[bhsa$otype == 'chapter' & bhsa$book == book & bhsa$chapter == chapter])
}
chapter2text = function(book, chapter) {
    return(object2text(chapter2object(book, chapter)))
}
# -

cat(verse2text('Psalmi', 131, 2))

cat(chapter2text('Psalmi', 131))

# # Bi-grams
#
# We make a column of verse-bound bi-grams of lexemes. The two lexemes are separated by an underscore `_`.

# +
vsNext = bhsa$in.verse[bhsa$otype=='word'][-1]
vsPrev = bhsa$in.verse[bhsa$otype=='word'][-length(bhsa)]

lex = bhsa$g_lex_utf8[bhsa$otype=='word']
lexNext = bhsa$g_lex_utf8[bhsa$otype=='word'][-1]
lastInVs = vsPrev != vsNext

lexNext[lastInVs] = ''

bigram = paste(
    lex,
    lexNext,
    sep='_'
)
# -

head(bigram, n=30)

vsNext[0:2]

vsPrev[0:2]

# + jupyter={"outputs_hidden": true}

