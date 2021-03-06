
import re
from common import RawLine, Reader
from comparators import RegexComparator, StringComparator
from common import RawGrammarReader

class GrammarDefiniensLine:

    def __init__(self, content):
        self.content = content
    
    def pattern(self):
        return re.findall('[\w:]+', self.content)[0]
    
    def has_tree_reference(self):
        return '->' in self.content
    
    def tree_reference(self):
        if not '->' in self.content:
            raise BaseException("This line has no tree reference")
        else:
            return self.content.split('->', 1)[1]
        
        
class GrammarDefinition:
    
    def __init__(self, tree_id):
        self.tree_id = tree_id
        self.definiens = []
    
    def add_definiens(self, line):
        self.definiens += [GrammarDefiniensLine(line)]
        
    def size(self):
        return len(self.definiens)


class GrammarLine(RawLine):
    def __init__(self, line):
        super(GrammarLine, self).__init__(line)
        self.indent.indent_size = 2


class GrammarDefinitionReader(RawGrammarReader):
    
    def __iter__(self):
        return self
    
    def next(self):
        if self.eof():
            raise StopIteration
        else:
            name = self.readline()
            if name.level() != 0:
                raise SyntaxError("Should be Tree name, level 0")
            grammar_def = GrammarDefinition(name.content)
            while not self.eof():
                definiens = self.readline()
                if definiens.level() == 0:
                    self.push(definiens)
                    break
                elif definiens.level() != 1:
                    raise SyntaxError("Should be Tree definiens, level 1")
                grammar_def.add_definiens(definiens.content)
            if grammar_def.size() < 1:
                raise SyntaxError("There should be at least one child line for a definition")
            return grammar_def
    
    def push(self, grammar_line):
        super(GrammarDefinitionReader, self).push(grammar_line.content)
    
class Stack:
    def __init__(self):
        self.stack = []
    
    def pop(self):
        return self.stack.pop()
    
    def push(self, node):
        return self.stack.append(node)
    
    def last(self):
        return self.stack[-1]
    
    def level(self):
        return len(self.stack) - 1

    
class BaseNode(object):
    
    def __init__(self, str):
        if '$' in str:
            self.comparator = RegexComparator(str[1:])
        else:
            self.comparator = StringComparator(str)
    
    def match(self, str):
        return self.comparator.compare(str)
    
    def traverse(self, tokens):
        raise NotImplementedError()
    
    def has_tree_reference(self):
        raise NotImplementedError()


class TranslationLeaf(BaseNode):
    
    def __init__(self, pattern, translation):
        super(TranslationLeaf, self).__init__(pattern)
        self.translation = translation
    
    def translation(self):
        return self.translation
    
    
class TreeReferenceNode(BaseNode):
    
    def __init__(self, pattern, tree_name):
        super(TreeReferenceNode, self).__init__(pattern)
        self._tree_name = tree_name
    
    def tree_name(self):
        return self._tree_name


class GrammarTree():
    def __init__(self):
        self.children = []
    
    def adopt(self, node):
        self.children.append(node)
        
    def find(self, line):
        for child in self.children:
            if child.match(line):
                return child


class GrammarForest:
    def __init__(self, file):
        self.roots = {}
        self.build(file)
    
    def build(self, file):
        for definition in GrammarDefinitionReader(file):
            self.add_definition(definition)
    
    def add_definition(self, definition):
        tree = GrammarTree()
        self.roots[definition.tree_id] = tree
        for line in definition.definiens: 
            if line.has_tree_reference():
                tree.adopt(TreeReferenceNode(line.pattern(), line.tree_reference()))
                
    def main_root(self):
        return self.roots['Root']


class GrammarTranslator:
    def __init__(self, syntax_forest):
        self.syntax_forest = syntax_forest
        self.stack = Stack()
        self.stack.push(syntax_forest.main_root())
    
    def up(self):
        self.stack.pop()
        
    def translate(self, line):
        node = self.stack.last().find(line.content)
        if not node.has_translation():
            tree = self.syntax_forest.roots[node.tree_name()]
            self.stack.push(tree)
        return node
        