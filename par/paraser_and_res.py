from lex.tokens import *
from err.error import *
from par.ast_node import *


"""
语法解析结果
"""


class ParserResult(object):
    def __init__(self):
        self.error = None
        self.node = None
        self.advance_count = 0

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        self.error = error
        return self

    def register_advancement(self):
        self.advance_count += 1

    def register(self, res):
        self.advance_count += res.advance_count
        if res.error:
            self.error = res.error
        return res.node

    def copy(self):
        result = ParserResult()
        result.error = self.error
        result.node = self.node
        result.advance_count = self.advance_count
        return result


"""
语法解析器
"""


class Parser(object):
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_idx = -1
        self.current_tok = None
        self.advance()

    def advance(self):
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]
        return self.current_tok

    def copy(self):     # 当前self备份
        result = Parser(self.tokens)
        result.tokens = self.tokens
        result.current_tok = self.current_tok
        result.tok_idx = self.tok_idx
        return result

    def bk_copy(self, result):      # 备份还原
        self.tokens = result.tokens
        self.current_tok = result.current_tok
        self.tok_idx = result.tok_idx

    def parse(self):
        res = self.program()
        if not res.error and self.current_tok.type != TT_EOF:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "parse Wrong "
            ))
        return res

    def program(self):
        res = ParserResult()

        if not self.current_tok.matches(TT_KEYWORDS, 'program'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected program "
            ))
        res.register_advancement()
        self.advance()

        if not self.current_tok.type == TT_IDENTIFIER:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected program's identifier "
            ))
        idt = VarAccessNode(self.current_tok)
        res.register_advancement()
        self.advance()

        if not self.current_tok.type == TT_FH:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected program's; "
            ))
        res.register_advancement()
        self.advance()
        block = res.register(self.block())
        if res.error:
            return res
        return res.success(ProgramNode(idt=idt, block=block))

    def block(self):
        res = ParserResult()
        pos_start = self.current_tok.pos_start
        type_definition_part = res.register(self.type_definition_part())
        if res.error:
            return res

        variable_declaration_part = res.register(self.variable_declaration_part())
        if res.error:
            return res

        procedure_and_function_declaration_part = res.register(self.procedure_and_function_declaration_part())
        if res.error:
            return res

        statement_part = res.register(self.statement_part())
        if res.error:
            return res

        return res.success(BlockNode(type_definition_part, variable_declaration_part,
                                     procedure_and_function_declaration_part, statement_part, pos_start))

    def type_definition_part(self):
        res = ParserResult()
        pos_start = self.current_tok.pos_start
        type_list = []
        if self.current_tok.matches(TT_KEYWORDS, 'type'):
            res.register_advancement()
            self.advance()
            while self.current_tok.value not in ('var', 'function', 'procedure', 'begin', 'end'):
                type_list.append(res.register(self.type_definition()))
                if res.error:
                    return res

                if self.current_tok.type is not TT_FH:
                    return res.failure(InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        "; "
                     ))
                res.register_advancement()
                self.advance()

        return res.success(Type_definition_partNode(type_list, pos_start))

    def type_definition(self):
        res = ParserResult()
        if self.current_tok.type is not TT_IDENTIFIER:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "type_definition IDENTIFIER"
            ))
        idt = self.current_tok
        res.register_advancement()
        self.advance()

        if self.current_tok.type is not TT_EQ:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "type_definition = "
            ))
        res.register_advancement()
        self.advance()

        type_ = res.register(self.type_())
        if res.error:
            return res
        return res.success(Type_definitionNode(idt, type_))

    def type_(self):
        # #<type>
        #     ::= <simple type> | <structured type>
        res = ParserResult()
        if not self.current_tok.matches(TT_KEYWORDS, 'class'):
            simple_type = res.register(self.simple_type())
            if res.error:
                return res
            return res.success(Type__Node(simple_type))
        structured_type = res.register(self.structured_type())
        if res.error:
            return res
        return res.success(Type__Node(structured_type))

    def simple_type(self):
        res = ParserResult()
        if self.current_tok.matches(TT_KEYWORDS, 'integer'):
            type_ = 'integer'

            return res.success(Simple_typeNode(type_, self.current_tok.pos_start))
        elif self.current_tok.matches(TT_KEYWORDS, 'real'):
            type_ = 'real'

            return res.success(Simple_typeNode(type_, self.current_tok.pos_start))
        return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                " integer or real "
            ))

    def structured_type(self):
        res = ParserResult()
        if not self.current_tok.matches(TT_KEYWORDS, 'class'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "class "
            ))
        res.register_advancement()
        self.advance()

        public_part = res.register(self.public_part())
        if res.error:
            return res
        if not self.current_tok.matches(TT_KEYWORDS, 'end'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "end ;"
            ))
        res.register_advancement()
        self.advance()

        # private_part = res.register(self.private_part())
        # protected_part = res.register(self.protected_part())
        return res.success(StructuredNode(public_part))     # ,private_part, protected_part))

    def public_part(self):
        res = ParserResult()
        if self.current_tok.matches(TT_KEYWORDS, 'public'):
            res.register_advancement()
            self.advance()
            var = res.register(self.variable_declaration_part())
            if res.error:
                return res
            pro = res.register(self.procedure_and_function_declaration_part())
            if res.error:
                return res
        return res.success(PublicNode(var, pro))

    def private_part(self):
        pass

    def protected_part(self):
        pass

    def variable_declaration_part(self):
        res = ParserResult()
        pos_start = self.current_tok.pos_start
        var_list = []
        if self.current_tok.matches(TT_KEYWORDS, 'var'):
            res.register_advancement()
            self.advance()
            while self.current_tok.value not in ('function', 'procedure', 'begin', 'end') and\
                    self.current_tok.type is not TT_FH:
                var_list.append(res.register(self.variable_definition()))
                res.register_advancement()
                self.advance()
                if res.error:
                    return res

                if self.current_tok.type is not TT_FH:
                    return res.failure(InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        "; "
                     ))
                res.register_advancement()
                self.advance()

        return res.success(Variable_definition_partNode(var_list, pos_start))

    def variable_definition(self):
        res = ParserResult()
        idt = self.current_tok
        idt_list = []
        if self.current_tok.type is not TT_IDENTIFIER:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "type_definition IDENTIFIER"
            ))
        idt_list.append(self.current_tok)
        res.register_advancement()
        self.advance()

        while self.current_tok.type is TT_DH:
            res.register_advancement()
            self.advance()
            if self.current_tok.type is not TT_IDENTIFIER:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "type_definition IDENTIFIER"
                ))
            idt_list.append(self.current_tok)
            res.register_advancement()
            self.advance()

        if self.current_tok.type is not TT_MH:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                " : "
            ))
        res.register_advancement()
        self.advance()

        if not self.current_tok.matches(TT_KEYWORDS, 'class'):
            if self.current_tok.type is not TT_IDENTIFIER:
                # simple_type
                simple_type = res.register(self.simple_type())
                if res.error:
                    return res

                return res.success(Variable_definitionNode(idt_list, 'simple_type', idt.pos_start))
            # identifier self_type
            idt = self.current_tok
            return res.success(Variable_definitionNode(idt_list, idt.value+',self_type', idt.pos_start))

        # class
        res.register_advancement()
        self.advance()

        if self.current_tok.type is not TT_IDENTIFIER:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                " class identifier"
            ))
        return res.success(Variable_definitionNode(idt_list, 'class', idt.pos_start))

    def procedure_and_function_declaration_part(self):
        res = ParserResult()
        pro_and_func_list = []
        pos_start = self.current_tok.pos_start
        while self.current_tok.value not in ('begin', 'end'):
            pro_and_func_list.append(self.procedure_and_function_declaration())
            if res.error:
                return res
        return res.success(Procedure_and_function_declaration_partNode(pro_and_func_list, pos_start))

    def procedure_and_function_declaration(self):
        # function
        res = ParserResult()
        pos_start = self.current_tok.pos_start
        if self.current_tok.matches(TT_KEYWORDS, 'function'):
            func = res.register(self.function_declaration())
            if res.error:
                return res
            return res.success(Procedure_and_function_declarationNode(func, pos_start))
        # procedure
        elif self.current_tok.matches(TT_KEYWORDS, 'procedure'):
            pro = res.register(self.procedure_declaration())
            if res.error:
                return res
            return res.success(Procedure_and_function_declarationNode(pro, pos_start))

    def procedure_declaration(self):
        # #<procedure declaration>
        #     ::= <procedure heading> ( <procedure body> )
        res = ParserResult()
        procedure_heading = res.register(self.procedure_heading())
        if res.error:
            return res
        procedure_body = res.register(self.procedure_body())
        if res.error:
            return res
        return res.success(Procedure_declarationNode(procedure_heading, procedure_body))

    def procedure_heading(self):
        # #<procedure heading>
        #     ::=
        #     procedure <identifier> '(' <formal parameter section>
        #     {;<formal parameter section>} ')';{<control_part>;}
        res = ParserResult()
        formal_parameter_section_list = []
        control_part_list = []
        if not self.current_tok.matches(TT_KEYWORDS, 'procedure'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected procedure "
            ))
        res.register_advancement()
        self.advance()
        if self.current_tok.type is not TT_IDENTIFIER:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected procedure' name "
            ))
        pro_name_tok = self.current_tok
        res.register_advancement()
        self.advance()
        if self.current_tok.type is TT_L:
            res.register_advancement()
            self.advance()
            if self.current_tok.type is not TT_R:
                formal_parameter_section_list.append(res.register(self.variable_definition()))
                # < variable declaration > == <formal parameter section>
                res.register_advancement()
                self.advance()
                if res.error:
                    return res
                while self.current_tok.type is TT_FH:
                    res.register_advancement()
                    self.advance()
                    formal_parameter_section_list.append(res.register(self.variable_definition()))
                    # < variable declaration > == <formal parameter section>
                    if res.error:
                        return res
                    res.register_advancement()
                    self.advance()

                    res.register_advancement()
                    self.advance()
                if self.current_tok.type is not TT_R:
                    return res.failure(InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        "Expected ) "
                    ))
                res.register_advancement()
                self.advance()
                if self.current_tok.type is not TT_FH:
                    return res.failure(InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        "Expected ; "
                    ))
                res.register_advancement()
                self.advance()
            # control_part
            else:
                res.register_advancement()
                self.advance()

                if self.current_tok.type is not TT_FH:
                    return res.failure(InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        "Expected ; "
                    ))
                res.register_advancement()
                self.advance()

            while self.current_tok.type is TT_KEYWORDS and \
                    self.current_tok.value in ('virtual', 'override', 'overload'):
                control_part_list.append(self.current_tok)
                res.register_advancement()
                self.advance()
                if self.current_tok.type is not TT_FH:
                    return res.failure(InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        "Expected procedure ; "
                    ))
                res.register_advancement()
                self.advance()
            return res.success(Procedure_headingNode(
                pro_name_tok, formal_parameter_section_list, control_part_list))
        return res.failure(InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        "Expected ( "
                    ))

    def procedure_body(self):
        # #<procedure body>
        #     := begin <commands> end;
        res = ParserResult()
        copy = self.copy()
        if self.current_tok.matches(TT_KEYWORDS, 'begin'):
            pos_start = self.current_tok.pos_start
            res.register_advancement()
            self.advance()
            commands = res.register(self.commands())
            if res.error:
                return res
            if self.current_tok.matches(TT_KEYWORDS, 'end'):
                res.register_advancement()
                self.advance()
                if self.current_tok.type is TT_FH:
                    res.register_advancement()
                    self.advance()
                    return res.success(Procedure_bodyNode(pos_start, commands))
                else:   # failure
                    self.bk_copy(copy)
                    return res.success(Procedure_bodyNode(self.current_tok.pos_start, commands))
        return res.success(Procedure_bodyNode(self.current_tok.pos_start))

    def function_declaration(self):
        pass

    def function_heading(self):
        pass

    def function_body(self):
        pass

    def statement_part(self):
        # #<statement part>
        #     ::=begin <commands> end.
        res = ParserResult()
        pos_start = self.current_tok.pos_start
        if not self.current_tok.matches(TT_KEYWORDS, 'begin'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected statement's begin "
            ))
        res.register_advancement()
        self.advance()

        commands = res.register(self.commands())
        if res.error:
            return res

        if self.current_tok.matches(TT_KEYWORDS, 'end'):
            res.register_advancement()
            self.advance()

            if self.current_tok.type is TT_GH:
                res.register_advancement()
                self.advance()

                pos_end = self.current_tok.pos_end
                return res.success(Statement_partNode(pos_start, pos_end, commands))
        return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected statement's end "
            ))

    def commands(self):
        # #<commands>
        #     := <command>;
        #     |  <command>; <commands>
        res = ParserResult()
        command_list = []
        while not self.current_tok.matches(TT_KEYWORDS, 'end'):
            temp = self.command()
            if temp is None:
                return res.success(CommandsNode(self.current_tok.pos_start, command_list))
            else:
                command_list.append(temp)
            if self.current_tok.type is not TT_FH:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected ;"
                ))
            res.register_advancement()
            self.advance()

        return res.success(CommandsNode(self.current_tok.pos_start, command_list))

    def command(self):
        # #<command>
        #     ::= <identifier> = <expr>|<identifier>
        #     | begin <commands> end
        #     | if <le_expr> then <command> else <command> end
        res = ParserResult()
        if self.current_tok.type is TT_IDENTIFIER:
            idt = self.current_tok
            res.register_advancement()
            self.advance()
            if self.current_tok.type is TT_EQ:
                res.register_advancement()
                self.advance()
                if self.current_tok.type is TT_IDENTIFIER:
                    expr = self.current_tok
                    res.register_advancement()
                    self.advance()
                    return res.success(CommandNode(idt, expr))
                else:
                    expr = res.register(self.expr())
                    if res.error:
                        return res
                    return res.success(CommandNode(idt, expr))

        if self.current_tok.matches(TT_KEYWORDS, 'if'):
            res.register_advancement()
            self.advance()
            le_expr = res.register(self.lexp())
            if res.error:
                return res
            if self.current_tok.matches(TT_KEYWORDS, 'then'):
                res.register_advancement()
                self.advance()
                command_if = res.register(self.command())
                if res.error:
                    return res
                if self.current_tok.matches(TT_KEYWORDS, 'else'):
                    res.register_advancement()
                    self.advance()
                    command_else = res.register(self.command())
                    if res.error:
                        return res
                    if self.current_tok.matches(TT_KEYWORDS, 'end'):
                        res.register_advancement()
                        self.advance()
                    return res.success(IfNode(le_expr, command_if, command_else))
                else:
                    if self.current_tok.matches(TT_KEYWORDS, 'end'):
                        res.register_advancement()
                        self.advance()
                    return res.success(IfNode(le_expr, command_if))

        if self.current_tok.matches(TT_KEYWORDS, 'begin'):
            pos_start = self.current_tok.pos_start
            res.register_advancement()
            self.advance()
            commands = res.register(self.commands())
            if self.current_tok.matches(TT_KEYWORDS, 'end'):
                pos_end = self.current_tok.pos_end
                res.register_advancement()
                self.advance()
                return res.success(Begin_commands_endNode(commands, pos_start, pos_end))

    def lexp(self):
        # #<lexp>
        #     := <expr> <lop> <expr>
        return self.bin_op(self.expr, (TT_EQ, TT_NE))

    def expr(self):
        # #<expr>
        #     := <term>{<aop><term>}
        return self.bin_op(self.term, (TT_MINUS, TT_PLUS))

    def term(self):
        # #<term>
        #     := <factor>{<mop><factor>}
        return self.bin_op(self.factor, (TT_MUL, TT_DIV))

    def factor(self):
        # #<factor>
        #     := <identifier>
        #     |<integer>
        #     |<real>
        res = ParserResult()
        tok = self.current_tok
        self.advance()
        if tok.type == TT_IDENTIFIER:
            return res.success(VarAccessNode(tok))
        elif tok.type == TT_INT or tok.type == TT_REAL:
            return res.success(NumberNode(tok))

    def bin_op(self, func_a, ops, func_b=None):
        if func_b is None:
            func_b = func_a

        res = ParserResult()
        left = res.register(func_a())
        if res.error:
            return res
        while self.current_tok.type in ops or (self.current_tok.type, self.current_tok.value) in ops:
            op_tok = self.current_tok
            res.register_advancement()
            self.advance()
            right = res.register(func_b())
            if res.error:
                return res
            left = BinOpNode(left, op_tok, right)
        return res.success(left)
