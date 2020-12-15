

"""
语法解析
"""


class ProgramNode(object):
    def __init__(self, idt, block):
        self.idt = idt
        self.block = block
        self.pos_start = idt.pos_start
        self.pos_end = block.pos_end

    def __repr__(self):
        result = ''
        result += f"program {self.idt} ; \n"
        result += f" {self.block}"
        return f'({result})'


class BlockNode(object):
    def __init__(self, type_definition_part, variable_declaration_part,
                 procedure_and_function_declaration_part, statement_part, pos_start):
        self.type_definition_part = type_definition_part
        self.variable_declaration_part = variable_declaration_part
        self.procedure_and_function_declaration_part = procedure_and_function_declaration_part
        self.statement_part = statement_part
        if self.type_definition_part:
            self.pos_start = self.type_definition_part.pos_start
        elif self.variable_declaration_part:
            self.pos_start = self.tvariable_declaration_part.pos_start
        elif procedure_and_function_declaration_part:
            self.pos_start = self.procedure_and_function_declaration_part.pos_start
        elif self.statement_part:
            self.pos_start = self.statement_part.pos_start
        else:
            self.pos_start = pos_start
        self.pos_end = self.statement_part.pos_end

    def __repr__(self):
        result = ''
        result += f"<type definition part>{self.type_definition_part}\n"
        result += f"<variable declaration part>{self.variable_declaration_part}\n"
        result += f"<procedure_and_function_declaration_part>{self.procedure_and_function_declaration_part}\n"
        result += f"<statement_part>{self.statement_part}\n"
        return f'({result})'


class Type_definition_partNode(object):
    def __init__(self, type_list, pos_start):
        self.type_list = type_list
        if len(self.type_list) > 0:
            self.pos_start = self.type_list[0].pos_start
            self.pos_end = self.type_list[-1].pos_end
        else:
            self.pos_start = pos_start
            self.pos_end = pos_start

    def __repr__(self):
        result = ''
        for i, _ in enumerate(self.type_list):
            result += f"{self.type_list[i]}"
        return f'({result}\n)'


class Type_definitionNode(object):
    def __init__(self, idt, type_):
        self.idt = idt
        self.type_ = type_
        self.pos_start = idt.pos_start
        self.pos_end = type_.pos_end

    def __repr__(self):
        result = ''
        result += f"{self.idt.value} = {self.type_}"
        return f'\n(\t{result}\t)'


class Type__Node(object):
    def __init__(self, type_):
        self.type_ = type_
        self.pos_start = type_.pos_start
        self.pos_end = type_.pos_end

    def __repr__(self):
        result = ''
        result += f"{self.type_}"
        return f'\t{result}'


class Simple_typeNode(object):
    def __init__(self, simple_type_, pos_start):
        self.value = simple_type_
        self.pos_start = pos_start
        self.pos_end = pos_start

    def __repr__(self):
        result = ''
        result += f"{self.value}"
        return f'{result}'


class StructuredNode(object):
    def __init__(self, public_part):
        self.public_part = public_part
        self.pos_start = self.public_part.pos_start
        self.pos_end = self.public_part.pos_end

    def __repr__(self):
        result = ''
        result += f"public :{self.public_part}"
        return f'{result}'


class PublicNode(object):
    def __init__(self, var, pro):
        self.var = var
        self.pro = pro
        self.pos_start = self.var.pos_start
        self.pos_end = self.pro.pos_end

    def __repr__(self):
        result = ''
        result += f"{self.var}"
        result += f"{self.pro}"
        return f'{result}'


class Variable_definition_partNode(object):
    def __init__(self, var_list, pos_start):
        self.var_list = var_list
        if len(self.var_list) > 0:
            self.pos_start = self.var_list[0].pos_start
            self.pos_end = self.var_list[-1].pos_end
        else:
            self.pos_start = pos_start
            self.pos_end = pos_start

    def __repr__(self):
        result = ''
        for i, _ in enumerate(self.var_list):
            result += f"\n{self.var_list[i]}"
        return f'({result}\n)'


class Variable_definitionNode(object):
    def __init__(self, idt_list, type_, pos_start):
        self.idt_list = idt_list
        self.type_ = type_
        if len(self.idt_list) > 0:
            self.pos_start = self.idt_list[0].pos_start
            self.pos_end = self.idt_list[-1].pos_end
        else:
            self.pos_start = pos_start
            self.pos_end = pos_start

    def __repr__(self):
        result = ''
        for i, _ in enumerate(self.idt_list):
            if i != len(self.idt_list) - 1:
                result += f"{self.idt_list[i].value},"
            else:
                result += f"{self.idt_list[i].value}"
        result += f": {self.type_}"
        return f'({result})'


class Procedure_and_function_declaration_partNode(object):
    def __init__(self, pro_and_func_list, pos_start):
        self.pro_and_func_list = pro_and_func_list
        if len(pro_and_func_list) > 0:
            self.pos_start = pro_and_func_list[0].node.pos_start
            self.pos_end = pro_and_func_list[len(pro_and_func_list)-1].node.pos_end
        self.pos_start = pos_start
        self.pos_end = pos_start

    def __repr__(self):
        result = ''
        for i, _ in enumerate(self.pro_and_func_list):
            result += f"{self.pro_and_func_list[i].node}"
        return f'({result})'


class Procedure_and_function_declarationNode(object):
    def __init__(self, pro_or_func, pos_start):
        self.pro_or_func = pro_or_func
        self.pos_start = pos_start
        self.pos_start = self.pro_or_func.pos_start
        self.pos_end = self.pro_or_func.pos_end

    def __repr__(self):
        result = ''
        result += f'\n{self.pro_or_func}'
        return f'{result}'


class Procedure_declarationNode(object):
    def __init__(self, pro_heading, pro_body):
        self.pro_heading = pro_heading
        self.pro_body = pro_body
        if self.pro_body:
            self.pos_end = self.pro_body.pos_end
        self.pos_start = self.pro_heading.pos_start
        self.pos_end = self.pro_heading.pos_end

    def __repr__(self):
        result = ''
        result += f'{self.pro_heading}\n'
        result += f'{self. pro_body}'
        return f'{result}'


class Procedure_headingNode(object):
    def __init__(self, pro_name_tok, formal_parameter_section_list, control_part_list):
        self.pro_name_tok = pro_name_tok
        self.formal_parameter_section_list = formal_parameter_section_list
        self.control_part_list = control_part_list
        self.pos_start = self.pro_name_tok.pos_start
        self.pos_end = self.pro_name_tok.pos_end

    def __repr__(self):
        result = ''
        result += f'pro_name : {self.pro_name_tok.value}\n'
        result += f'formal_parameter : {self.formal_parameter_section_list}\n'
        for i, _ in enumerate(self.control_part_list):
            result += f"{self.control_part_list[i].value}"
        return f'{result}'


class Procedure_bodyNode(object):
    def __init__(self, pos_start, commands=None):
        if not commands:
            self.pos_start = pos_start
            self.pos_end = pos_start
            self.commands = commands
        else:
            self.commands = commands
            self.pos_start = commands.pos_start
            self.pos_end = commands.pos_end

    def __repr__(self):
        if not self.commands:
            return f''
        result = f'{self.commands}'
        return f'{result}'


class CommandsNode(object):
    def __init__(self, pos_start, command_list=None):
        if len(command_list) > 0:
            self.command_list = command_list
            self.pos_start = command_list[0].node.pos_start
            self.pos_end = command_list[-1].node.pos_end
        else:
            self.pos_start = pos_start
            self.pos_end = pos_start
            self.command_list = command_list

    def __repr__(self):
        if self.command_list is None:
            return ''
        result = ''
        for i, _ in enumerate(self.command_list):
            result += f"{self.command_list[i].node}" \
                      f";"
        return f'{result}'


class CommandNode(object):
    def __init__(self, idt=None, expr=None):
        self.idt = idt
        self.expr = expr
        self.pos_start = idt.pos_start
        self.pos_end = expr.pos_end

    def __repr__(self):
        result = ''
        result += f'{self.idt} , {self.expr}'
        return f'{result}'


class Statement_partNode(object):
    def __init__(self,  pos_start, pos_end, command_list=None):
        if not command_list:
            self.pos_start = pos_start
            self.pos_end = pos_end
        else:
            self.command_list = command_list
            self.pos_start = command_list.pos_start
            self.pos_end = command_list.pos_end

    def __repr__(self):
        result = '\n'
        result += f"\tbegin \n"
        result += f'{self.command_list}'
        result += f"\nend."
        return f'({result})'


class EofNode(object):
    def __init__(self):
        pass

    def __repr__(self):
        result = ''
        return result


class NumberNode(object):
    # 数字节点
    def __init__(self, tok):
        self.tok = tok
        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end

    def __repr__(self):
        return f'{self.tok}'


class BinOpNode(object):
    # 二元操作： + - * /  1 + 1      left_node:1 op_tok:+ right_node:1
    def __init__(self, left_node, op_tok, right_node):
        self.left_node = left_node
        self.pos_start = self.left_node.pos_start
        self.op_tok = op_tok
        self.right_node = right_node
        self.pos_end = self.right_node.pos_start

    def __repr__(self):
        return f'({self.left_node}, {self.op_tok}, {self.right_node})'


class UnaryOpNode(object):
    # 一元操作： -1 op_tok:- node 1
    def __init__(self, op_tok, node):
        self.op_tok = op_tok
        self.node = node

    def __repr__(self):
        return f'({self.op_tok}, {self.node})'


class VarAccessNode(object):
    # 访问var
    def __init__(self, var_name_tok):
        self.var_name_tok = var_name_tok
        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.var_name_tok.pos_end

    def __repr__(self):
        return f'({self.var_name_tok})'


class VarAssignNode(object):
    # 为var分配值
    def __init__(self, var_name_tok, value_node):
        self.var_name_tok = var_name_tok
        self.value_node = value_node
        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.var_name_tok.pos_end

    def __repr__(self):
        return f'({self.var_name_tok}, {self.value_node})'


class IfNode(object):
    def __init__(self, le_expr, command_if, command_else=None):
        self.le_expr = le_expr
        self.command_if = command_if
        self.command_else = command_else
        self.pos_start = self.le_expr.pos_start
        if self.command_else is not None:
            self.pos_end = self.command_else.pos_end
        else:
            self.pos_end = self.command_if.pos_end

    def __repr__(self):
        result = ''
        result += f'if:{self.le_expr}\n'
        result += f'then({self.command_if})\n'
        if self.command_else is not None:
            result += f'else {self.command_else} end'
        else:
            result += ' end'
        return f'({result})'


class Begin_commands_endNode(object):
    def __init__(self, commands, pos_start, pos_end):
        self.commands = commands
        self.pos_start = pos_start
        self.pos_end = pos_end

    def __repr__(self):
        return f'({self.commands})'


class ForNode(object):
    def __init__(self, value_name_tok, start_value_node, end_value_node, step_value_node, body_node):
        self.value_name_tok = value_name_tok
        self.start_value_node = start_value_node
        self.end_value_node = end_value_node
        self.step_value_node = step_value_node
        self.body_node = body_node
        self.pos_start = self.value_name_tok.pos_start
        self.pos_end = self.body_node.pos_end

    def __repr__(self):
        result = ''
        result += f"for {self.value_name_tok} = {self.start_value_node} "
        result += f"to {self.end_value_node} step {self.step_value_node} "
        result += f"then {self.body_node}"
        return f'({result})'


class WhileNode(object):
    def __init__(self, condition_node, body_node):
        self.condition_node = condition_node
        self.body_node = body_node
        self.pos_start = self.condition_node.left_node.pos_start
        self.pos_end = self.body_node.pos_end

    def __repr__(self):
        result = ''
        result += f"while {self.condition_node} then "
        result += f" {self.body_node}"
        return f'({result})'


class FunctionNode(object):
    def __init__(self, function_name_tok, arg_name_tokens, body_node):
        self.function_name_tok = function_name_tok
        self.arg_name_tokens = arg_name_tokens
        self.body_node = body_node
        if self.function_name_tok:
            self.pos_start = self.function_name_tok.pos_start
        elif len(self.arg_name_tokens) > 0:
            self.pos_start = self.arg_name_tokens[0].pos_start
        else:
            self.pos_start = self.body_node.pos_start

        self.pos_end = self.body_node.pos_end

    def __repr__(self):
        result = ''
        result += f"function then "
        result += f" {self.body_node}"
        return f'({result})'


class CallNode(object):
    def __init__(self, node_to_cal, arg_nodes):
        self.node_to_cal = node_to_cal
        self.arg_nodes = arg_nodes
        self.pos_start = self.node_to_cal.pos_start
        if len(self.arg_nodes) > 0:
            self.pos_end = self.arg_nodes[len(self.arg_nodes) - 1].pos_end
        else:
            self.pos_end = self.node_to_cal.pos_end

