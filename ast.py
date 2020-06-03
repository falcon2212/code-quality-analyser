import pycparser as pycparser
from pycparser import parse_file, c_generator
# from inspect import get_functions



ast = parse_file("1.c", use_cpp=True)
ast.show()
def get_source_string(node):
	return c_generator.CGenerator().visit(node)
def translate_to_c(filename):
    """ Simply use the c_generator module to emit a parsed AST.
    """
    ast = parse_file(filename, use_cpp=True)
    generator = c_generator.CGenerator()
    print(generator.visit(ast)) 
# def get_source_document(ast):
# 	if(ast.type)
child = ast.children()
# v = FuncDefVisitor()
# v.visit(ast)
for i in child:
	print type(i[1])
print type(child[1]), translate_to_c("1.c")
print type(ast.ext)
l = ast.ext
for i in l:
	print type(i), isinstance(i, pycparser.c_ast.FuncDef)
	print "function",i.decl.name, get_source_string(i.decl)
	# print i.body.block_items
	for j in i.body.block_items:
		if(isinstance(j, pycparser.c_ast.While)):
			print "while"
			# for k in j.stmt.block_items:
			# 	print k
			print c_generator.CGenerator().visit(j)
		elif isinstance(j, pycparser.c_ast.If):
			print "If block"
			print type(j.iftrue)
			print isinstance(j.iftrue, pycparser.c_ast.EmptyStatement)
			# print c_generator.CGenerator().visit(j.iffalse)
		elif isinstance(j, pycparser.c_ast.FuncCall):
			print "function call"		
		elif isinstance(j, pycparser.c_ast.FuncDef):
			print "function definition", j,get_source_string(j)	
		elif isinstance(j, pycparser.c_ast.Decl):
			print "declaration"		
		elif isinstance(j, pycparser.c_ast.Assignment):
			print "assignment"
		elif isinstance(j, pycparser.c_ast.Return):
			print "return", get_source_string(j)		
		else:
			print type(j)
	# for j in i.ext:
	# 	print j
