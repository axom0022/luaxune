import re

class parser:
    def parse(self, code):
        tokens = self.tokenize(code)
        return self.buildast(tokens)

    def tokenize(self, code):
        patterns = {
            'COMMENT': r'--[^\n]*',
            'STRING': r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'',
            'NUMBER': r'\b\d+\.?\d*(?:[eE][+-]?\d+)?\b',
            'KEYWORD': r'\b(?:and|break|do|else|elseif|end|false|for|function|if|in|local|nil|not|or|repeat|return|then|true|until|while)\b',
            'IDENTIFIER': r'[a-zA-Z_][a-zA-Z0-9_]*',
            'OPERATOR': r'[+\-*/%^#=<>~&|!():;{},.\[\]]+',
            'WHITESPACE': r'\s+',
        }
        combined = '|'.join(f'(?P<{name}>{pat})' for name, pat in patterns.items())
        tokens = []
        for m in re.finditer(combined, code):
            kind = m.lastgroup
            if kind == 'WHITESPACE' or kind == 'COMMENT':
                continue
            tokens.append((kind, m.group()))
        return tokens

    def buildast(self, tokens):
        ast = {'type': 'chunk', 'body': []}
        i = 0
        while i < len(tokens):
            tok = tokens[i]
            if tok[0] == 'KEYWORD':
                if tok[1] == 'local':
                    i = self.parselocal(tokens, i, ast)
                elif tok[1] == 'function':
                    i = self.parsefuncdef(tokens, i, ast)
                elif tok[1] == 'if':
                    i = self.parseif(tokens, i, ast)
                elif tok[1] == 'while':
                    i = self.parsewhile(tokens, i, ast)
                elif tok[1] == 'for':
                    i = self.parsefor(tokens, i, ast)
                elif tok[1] == 'repeat':
                    i = self.parserepeat(tokens, i, ast)
                elif tok[1] == 'return':
                    i = self.parsereturn(tokens, i, ast)
                else:
                    i += 1
            else:
                i = self.parseexprstmt(tokens, i, ast)
        return ast

    def parselocal(self, tokens, i, ast):
        i += 1
        names = []
        types = []
        while i < len(tokens) and tokens[i][0] in ('IDENTIFIER', ','):
            if tokens[i][0] == 'IDENTIFIER':
                name = tokens[i][1]
                i += 1
                typ = None
                if i < len(tokens) and tokens[i][0] == 'OPERATOR' and tokens[i][1] == ':':
                    i += 1
                    typ, i = self._parse_type(tokens, i)
                names.append(name)
                types.append(typ)
            else:
                i += 1
        exprs = []
        if i < len(tokens) and tokens[i][0] == 'OPERATOR' and tokens[i][1] == '=':
            i += 1
            while i < len(tokens) and not (tokens[i][0] == 'KEYWORD' and tokens[i][1] in ('end', 'else', 'elseif')):
                expr, i = self.parseexpr(tokens, i)
                exprs.append(expr)
                if i < len(tokens) and tokens[i][0] == 'OPERATOR' and tokens[i][1] == ',':
                    i += 1
        if not exprs:
            exprs = [None] * len(names)
        ast['body'].append({'type': 'local', 'names': names, 'types': types, 'values': exprs})
        return i

    def parsefuncdef(self, tokens, i, ast):
        i += 1
        name = tokens[i][1] if tokens[i][0] == 'IDENTIFIER' else None
        if name:
            i += 1
        if i < len(tokens) and tokens[i][0] == 'OPERATOR' and tokens[i][1] == '(':
            i += 1
            params = []
            paramtypes = []
            while i < len(tokens) and not (tokens[i][0] == 'OPERATOR' and tokens[i][1] == ')'):
                if tokens[i][0] == 'IDENTIFIER':
                    pname = tokens[i][1]
                    i += 1
                    ptype = None
                    if i < len(tokens) and tokens[i][0] == 'OPERATOR' and tokens[i][1] == ':':
                        i += 1
                        ptype, i = self._parse_type(tokens, i)
                    params.append(pname)
                    paramtypes.append(ptype)
                    if i < len(tokens) and tokens[i][0] == 'OPERATOR' and tokens[i][1] == ',':
                        i += 1
                else:
                    i += 1
            if i < len(tokens) and tokens[i][1] == ')':
                i += 1
        rettype = None
        if i < len(tokens) and tokens[i][0] == 'OPERATOR' and tokens[i][1] == ':':
            i += 1
            rettype, i = self._parse_type(tokens, i)
        body = []
        while i < len(tokens) and not (tokens[i][0] == 'KEYWORD' and tokens[i][1] == 'end'):
            if tokens[i][0] == 'KEYWORD' and tokens[i][1] == 'return':
                ret, i = self.parsereturn(tokens, i, None)
                body.append(ret)
            else:
                stmt, i = self.parsestmt(tokens, i)
                body.append(stmt)
        if i < len(tokens) and tokens[i][1] == 'end':
            i += 1
        ast['body'].append({'type': 'function', 'name': name, 'params': params, 'paramtypes': paramtypes, 'rettype': rettype, 'body': body})
        return i

    def _parse_type(self, tokens, i):
        if i < len(tokens) and tokens[i][0] == 'IDENTIFIER':
            typ = tokens[i][1]
            i += 1
            return typ, i
        return None, i

    def parseif(self, tokens, i, ast):
        i += 1
        cond, i = self.parseexpr(tokens, i)
        if i < len(tokens) and tokens[i][0] == 'KEYWORD' and tokens[i][1] == 'then':
            i += 1
        thenbody = []
        while i < len(tokens) and not (tokens[i][0] == 'KEYWORD' and tokens[i][1] in ('else', 'elseif', 'end')):
            stmt, i = self.parsestmt(tokens, i)
            thenbody.append(stmt)
        elsebody = []
        if i < len(tokens) and tokens[i][0] == 'KEYWORD' and tokens[i][1] == 'else':
            i += 1
            while i < len(tokens) and not (tokens[i][0] == 'KEYWORD' and tokens[i][1] == 'end'):
                stmt, i = self.parsestmt(tokens, i)
                elsebody.append(stmt)
        if i < len(tokens) and tokens[i][1] == 'end':
            i += 1
        ast['body'].append({'type': 'if', 'condition': cond, 'then': thenbody, 'else': elsebody})
        return i

    def parsewhile(self, tokens, i, ast):
        i += 1
        cond, i = self.parseexpr(tokens, i)
        if i < len(tokens) and tokens[i][0] == 'KEYWORD' and tokens[i][1] == 'do':
            i += 1
        body = []
        while i < len(tokens) and not (tokens[i][0] == 'KEYWORD' and tokens[i][1] == 'end'):
            stmt, i = self.parsestmt(tokens, i)
            body.append(stmt)
        if i < len(tokens) and tokens[i][1] == 'end':
            i += 1
        ast['body'].append({'type': 'while', 'condition': cond, 'body': body})
        return i

    def parsefor(self, tokens, i, ast):
        i += 1
        var = tokens[i][1] if tokens[i][0] == 'IDENTIFIER' else None
        i += 1
        if i < len(tokens) and tokens[i][0] == 'OPERATOR' and tokens[i][1] == '=':
            i += 1
            start, i = self.parseexpr(tokens, i)
            if i < len(tokens) and tokens[i][0] == 'OPERATOR' and tokens[i][1] == ',':
                i += 1
            end, i = self.parseexpr(tokens, i)
            step = None
            if i < len(tokens) and tokens[i][0] == 'OPERATOR' and tokens[i][1] == ',':
                i += 1
                step, i = self.parseexpr(tokens, i)
        if i < len(tokens) and tokens[i][0] == 'KEYWORD' and tokens[i][1] == 'do':
            i += 1
        body = []
        while i < len(tokens) and not (tokens[i][0] == 'KEYWORD' and tokens[i][1] == 'end'):
            stmt, i = self.parsestmt(tokens, i)
            body.append(stmt)
        if i < len(tokens) and tokens[i][1] == 'end':
            i += 1
        ast['body'].append({'type': 'for', 'var': var, 'start': start, 'end': end, 'step': step, 'body': body})
        return i

    def parserepeat(self, tokens, i, ast):
        i += 1
        body = []
        while i < len(tokens) and not (tokens[i][0] == 'KEYWORD' and tokens[i][1] == 'until'):
            stmt, i = self.parsestmt(tokens, i)
            body.append(stmt)
        if i < len(tokens) and tokens[i][1] == 'until':
            i += 1
            cond, i = self.parseexpr(tokens, i)
        ast['body'].append({'type': 'repeat', 'condition': cond, 'body': body})
        return i

    def parsereturn(self, tokens, i, ast):
        i += 1
        values = []
        while i < len(tokens) and not (tokens[i][0] == 'KEYWORD' and tokens[i][1] in ('end', 'else', 'elseif')):
            if tokens[i][0] != 'OPERATOR' or tokens[i][1] != ',':
                expr, i = self.parseexpr(tokens, i)
                values.append(expr)
            else:
                i += 1
        if ast is None:
            return {'type': 'return', 'values': values}, i
        ast['body'].append({'type': 'return', 'values': values})
        return i

    def parsestmt(self, tokens, i):
        tok = tokens[i]
        if tok[0] == 'KEYWORD':
            if tok[1] == 'local':
                dummy = {'body': []}
                i = self.parselocal(tokens, i, dummy)
                return dummy['body'][0], i
            elif tok[1] == 'return':
                ret, i = self.parsereturn(tokens, i, None)
                return ret, i
            else:
                return {'type': 'expression', 'value': {'type': 'nil', 'value': None}}, i + 1
        else:
            expr, i = self.parseexpr(tokens, i)
            return {'type': 'expression', 'value': expr}, i

    def parseexprstmt(self, tokens, i, ast):
        expr, i = self.parseexpr(tokens, i)
        ast['body'].append({'type': 'expression', 'value': expr})
        return i

    def parseexpr(self, tokens, i):
        return self._parse_expr_prec(tokens, i, 0)

    def _parse_expr_prec(self, tokens, i, min_prec):
        lhs, i = self._parse_primary(tokens, i)
        if lhs is None:
            return {'type': 'nil', 'value': None}, i
        while True:
            if i >= len(tokens):
                break
            tok = tokens[i]
            if tok[0] != 'OPERATOR':
                break
            op = tok[1]
            prec = self._op_precedence(op)
            if prec < min_prec:
                break
            if op == '=':
                break
            i += 1
            rhs, i = self._parse_expr_prec(tokens, i, prec + 1)
            if rhs is None:
                break
            lhs = {'type': 'binop', 'op': op, 'left': lhs, 'right': rhs}
        return lhs, i

    def _op_precedence(self, op):
        if op in ('or',):
            return 1
        if op in ('and',):
            return 2
        if op in ('<', '>', '<=', '>=', '==', '~='):
            return 3
        if op in ('..',):
            return 4
        if op in ('+', '-'):
            return 5
        if op in ('*', '/', '%'):
            return 6
        if op in ('^',):
            return 7
        if op in ('.', ':', '['):
            return 8  
        return 0

    def _parse_primary(self, tokens, i):
        if i >= len(tokens):
            return None, i
        tok = tokens[i]
        if tok[0] == 'NUMBER':
            return {'type': 'number', 'value': float(tok[1])}, i+1
        elif tok[0] == 'STRING':
            return {'type': 'string', 'value': tok[1][1:-1]}, i+1
        elif tok[0] == 'IDENTIFIER':
            if tok[1] == 'true':
                return {'type': 'boolean', 'value': True}, i+1
            elif tok[1] == 'false':
                return {'type': 'boolean', 'value': False}, i+1
            elif tok[1] == 'nil':
                return {'type': 'nil', 'value': None}, i+1
            return {'type': 'identifier', 'value': tok[1]}, i+1
        elif tok[0] == 'OPERATOR':
            if tok[1] == '(':
                expr, i = self._parse_expr_prec(tokens, i+1, 0)
                if i < len(tokens) and tokens[i][1] == ')':
                    i += 1
                return {'type': 'grouped', 'value': expr}, i
            elif tok[1] == '.':
                return None, i
            elif tok[1] == '[':
                return None, i
            else:
                return None, i
        return None, i
