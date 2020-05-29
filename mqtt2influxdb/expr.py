import py_expression_eval
from schema import SchemaError


def jsonpath_to_variable(p):
    """Converts a JSON path starting with $. into a valid expression variable"""
    # replace $ with JSON_ and . with _
    return p.replace('$', 'JSON_').replace('.', '_')

def variable_to_jsonpath(p):
    """Converts a expression variable into a valid JSON path starting with $."""
    # replace JSON_ with $ and _ with .
    return p.var.replace('JSON_', '$').replace('_', '.')

def parse_expression(txt):
    """Parse the given expression and returns a parser object"""
    try:
        # remove leading =
        txt = txt.replace("=", "")
        return py_expression_eval.Parser().parse(jsonpath_to_variable(txt))
    except Exception as e:
        raise SchemaError('Bad expression format: %s' % txt)
