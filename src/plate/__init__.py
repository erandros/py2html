from lexical.structure import Statement

class TemplateParser():
    reader = None
    writer = None
    mainParser = None
    
    def __init__(self, mainParser):
        None
    ''' self.reader = mainParser.reader
        self.writer = mainParser.writer
        self.mainParser = mainParser'''
    
class Load(Statement):
    def tag(self, reader, params):
        return ""
'''class Inherit(Statement):
    def state(self, params):
        return "Inherited"
#        
class Override(Block):
    def open_block(self, params):
        Block.open_block(self, params)
    def close_block(self, params):
        Block.close_block(self, params)

class Symbol(): 
    content = ""
    def __init__(self, content):
        self.content = content

#class Tree():
#class TreeNode():
#    content = ""
#    sons 

#def process_templates(lines):
 #   for line in lines:
'''