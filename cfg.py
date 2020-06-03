import pycparser as pycparser
from pycparser import parse_file, c_generator
def get_source_string(node):
	return c_generator.CGenerator().visit(node)
class CfgNode(object):
	def __init__(self, statement = "", entry = False, exit = False):
		self.statement = statement
		self.adj_list = []
		self.enter = entry
		self.exit = exit

class Cfg(object):
	def __init__(self, ast):
		self.node = CfgNode(entry = True)	
		l = ast.ext
		start = self.node
		end = [start]
		function_graph = {}
		for i in l:
			# print i.decl.name
			st, en = self.function_build(i)
			function_graph[c_generator.CGenerator().visit(i.decl)] = (st, en)
			if i.decl.name == "main":
				start.adj_list.append(st)
				end = en
	def build_block(self, asst):
		j = asst
		if(isinstance(j, pycparser.c_ast.While)):
			# print "while"
			# print c_generator.CGenerator().visit(j)
			curr = CfgNode(get_source_string(j.cond))
			st1, en1 =self.build_block(j.stmt)
			curr.adj_list.append(st1)
			end = en1
			for i in end:
				i.adj_list.append(curr)
			end = [curr]
			return (curr, end)	
		elif isinstance(j, pycparser.c_ast.If):
			# print "If block"
			curr = CfgNode("if("+get_source_string(j.cond)+")")
			end = []
			# print j.iftrue	
			st1, en1 =self.build_block(j.iftrue)
			st1.statement = "{"+st1.statement
			for i in en1:
				i.statement = i.statement+"}"
			curr.adj_list.append(st1)
			end = end+en1
			if(j.iffalse == None):	
				end.append(curr)
			else:
				st2, en2 =self.build_block(j.iffalse)
				# print j.iffalse
				st2.statement = "else "+st2.statement
				# print  "else :sdf dsf ", st2.statement
				curr.adj_list.append(st2)
				end+=en2
			return (curr, end)
		elif isinstance(j, pycparser.c_ast.FuncCall):
			# print "function call"		
			curr = CfgNode(get_source_string(j))		
			end = [curr]
			return (curr, end)	
		elif isinstance(j, pycparser.c_ast.Decl):
			# print "declaration"
			curr = CfgNode(get_source_string(j))		
			end = [curr]
			return (curr, end)	
		elif isinstance(j, pycparser.c_ast.Assignment) or isinstance(j, pycparser.c_ast.EmptyStatement):
			# print "assignment"		
			curr = CfgNode(get_source_string(j))		
			end = [curr]
			return (curr, end)	
		elif isinstance(j, pycparser.c_ast.Return):
			# print "return", get_source_string(j)		
			curr = CfgNode(get_source_string(j))		
			end = [curr]
			return (curr, end)	
		elif isinstance(j, pycparser.c_ast.Compound):
			# print "compound", get_source_string(j)		
			curr = CfgNode(get_source_string(j))		
			end = [curr]
			return (curr, end)	
		else:
			print "Invalid type"
			# print type(j), get_source_string(j), j
			return (-1, -1)

	def function_build(self,asst):
		entry_node = CfgNode(get_source_string(asst.decl), entry = True)
		# asst.show()
		st, en = self.build_compound(asst)
		entry_node.adj_list.append(st)
		# print type(asst)
		return (entry_node, en)
	def build_compound(self, asst):	
		curr = None
		start = curr
		endp = []	
		for j in asst.body.block_items:
			st, en = self.build_block(j)
			if start == None:
				start = st
			for i in endp:
				i.adj_list.append(st)	
			endp = en
		return (start, endp)	

def dfs(node):
	print node.statement
	for i in node.adj_list:
		dfs(i)
if(__name__ == "__main__"):
	ast = parse_file("1.c", use_cpp=True)
	cfg = Cfg(ast)
	dfs(cfg.node)