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
		self.start = self.node
		self.end = [self.start]
		self.function_graph = {}
		for i in l:
			# print i.decl.name
			st, en, vertices, edges = self.function_build(i)
			self.function_graph[c_generator.CGenerator().visit(i.decl)] = (st, en, vertices, edges)
			if i.decl.name == "main":
				self.start.adj_list.append(st)
				self.end = en

	def build_block(self, asst):
		j = asst
		vertices = 0
		edges = 0
		if(isinstance(j, pycparser.c_ast.While)):
			curr = CfgNode("while "+get_source_string(j.cond))
			vertices+=1
			st1, en1, ver_res, edges_res =self.build_block(j.stmt)
			# print vertices, edges
			vertices += ver_res
			edges += edges_res
			curr.adj_list.append(st1)
			edges+=1
			end = en1
			for i in end:
				i.adj_list.append(curr)
				edges+=1
			end = [curr]
			return (curr, end, vertices, edges)	
		elif isinstance(j, pycparser.c_ast.If):
			curr = CfgNode("if "+get_source_string(j.cond))
			end = []
			# print j.iftrue	
			vertices+=1
			st1, en1, ver_res, edges_res =self.build_block(j.iftrue)
			vertices+=ver_res
			edges+=edges_res
			curr.adj_list.append(st1)
			edges+=1
			end = end+en1
			if(j.iffalse == None):	
				end.append(curr)
			else:
				st2, en2, ver_res, edges_res =self.build_block(j.iffalse)
				vertices+=ver_res
				edges+=edges_res
				# print j.iffalse
				st2.statement = "else "+st2.statement
				# print  "else :sdf dsf ", st2.statement
					# print i.statement,"sd"
				curr.adj_list.append(st2)
				edges+=1
				end+=en2
			return (curr, end, vertices, edges)	
		elif isinstance(j, pycparser.c_ast.FuncCall):
			# print "function call"		
			curr = CfgNode(get_source_string(j))	
			end = CfgNode()	
			curr.adj_list.append(end)
			vertices+=2
			edges+=1
			end = [end]
			return (curr, end, vertices, edges)	
		elif isinstance(j, pycparser.c_ast.Decl):
			# print "declaration"
			vertices+=2
			curr = CfgNode(get_source_string(j))	
			end = CfgNode()	
			curr.adj_list.append(end)
			end = [end]
			edges+=1
			return (curr, end, vertices, edges)	
		elif isinstance(j, pycparser.c_ast.Assignment) or isinstance(j, pycparser.c_ast.EmptyStatement):
			vertices=2
			curr = CfgNode(get_source_string(j))	
			end = CfgNode()	
			curr.adj_list.append(end)
			edges=1
			end = [end]
			return (curr, end, vertices, edges)	
		elif isinstance(j, pycparser.c_ast.Return):
			# print "return", get_source_string(j)		
			vertices+=2
			curr = CfgNode(get_source_string(j))	
			end = CfgNode()	
			curr.adj_list.append(end)
			edges+=1
			end = [end]
			return (curr, end, vertices, edges)	
		elif isinstance(j, pycparser.c_ast.Compound):
			# print "compound", get_source_string(j),j
			st, en, ver_res, edges_res = self.build_compound(j)		
			# curr = CfgNode(get_source_string(j))	
			# end = CfgNode()	
			# curr.adj_list.append(end)
			# end = [end]
			vertices+=ver_res
			edges+=edges_res
			return (st, en, vertices, edges)	
		else:
			print "Invalid type"
			# print type(j), get_source_string(j), j
			return (-1, -1, 0, 0)

	def function_build(self,asst):
		entry_node = CfgNode(get_source_string(asst.decl), entry = True)
		vertices = 2
		edges = 0
		# asst.show()
		st, en,ver_res,edges_res = self.build_compound(asst.body)
		entry_node.adj_list.append(st)
		edges+=1
		vertices+=ver_res
		edges+=edges_res
		exit_node = CfgNode(exit = False)
		for i in en:
			i.adj_list.append(exit_node)
			edges+=1	
		# print type(asst)
		return (entry_node, exit_node, vertices, edges)
	def build_compound(self, asst):	
		curr = None
		start = curr
		endp = []	
		vertices = 0
		edges = 0
		# print type(asst), asst
		for j in asst.block_items:
			# print j
			st, en, ver_res, edges_res = self.build_block(j)
			vertices+=ver_res
			edges+=edges_res
			if start == None:
				start = st
				endp = [start]
				vertices+=1
			for i in endp:
				i.adj_list.append(st)
				edges+=1
			endp = en
		return (start, endp, vertices, edges)	
	def print_cyclomatic_complexity(self):
		for i in self.function_graph:
			st, en, v, e = self.function_graph[i]
			print "Cyclomatic complexity of function '"+i+"' is = "+str(e-v+2)
def dfs(node):
	print node.statement
	for i in node.adj_list:
		dfs(i)
if(__name__ == "__main__"):
	ast = parse_file("1.c", use_cpp=True)
	cfg = Cfg(ast)
	cfg.print_cyclomatic_complexity()
	# dfs(cfg.node)