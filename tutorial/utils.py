def _parseTerminal(string):
    if ' ' in string:
        (tag, num) = string.split(' ', 1)
        return (tag, int(num))
    return string


def _parseBrackets(string):
    if string == '':
        return ([], '', None)
    if string[0] == '(':
        rest = string[1:]
        result = []
        error = None
        while rest != '' and rest[0] != ')':
            (thisResult, rest, error) = _parseBrackets(rest)
            if error:
                break
            result.append(thisResult)
        if rest == '':
            error = 'Missing ")" in "{}"'.format(string[1:])
        if len(rest):
            rest = rest[1:]
        return (result, rest, error)
    if string[0] == ')':
        return ('', string[1:], None)
    theOpen = string.find('(')
    theClose = string.find(')')
    if theOpen == -1 and theClose == -1:
        return (_parseTerminal(string), '', None)
    nextPos = None
    if theOpen == -1:
        nextPos = theClose
    else:
        nextPos = theOpen if theClose == -1 else min((theOpen, theClose))
    return (_parseTerminal(string[0:nextPos]), string[nextPos:], None)


def structure(string):
    (result, rest, error) = _parseBrackets(string)
    if error:
        return error
    if rest:
        return 'trailing material: "{}"'.format(rest)
    return result


_indentString = '  '


def _stringFromTerminal(terminal, terminalRep):
    if type(terminal) is str:
        return terminal
    return '{} {}'.format(
        terminal[0],
        terminalRep(terminal[1]),
    )


def _translate(func, shift):
    return lambda n: func(n + shift)


def _layout(structs, terminalRep, indent, withLevel):
    if type(structs) is str or type(structs) is tuple:
        return '{}{}{}'.format(
            '{:>2}'.format(indent)
            if withLevel else '', _indentString * indent,
            _stringFromTerminal(structs, terminalRep)
        )
    else:
        result = []
        for struct in structs:
            result.append(_layout(struct, terminalRep, indent + 1, withLevel))
        return '\n'.join(result)


def layout(structs, start, terminalRep, withLevel=False):
    theTerminalRep = _translate(terminalRep, start)
    return _layout(structs, theTerminalRep, 0, withLevel)
