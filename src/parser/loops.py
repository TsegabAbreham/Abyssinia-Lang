from node import *

class WhileLoopParser:
    def parse_while_loop(self):
        self.eat("WHILE")
        condition = self.parse_parens(self.parse_logical)
        self.eat("LBRACKET")
        body = self.parse_block()

        return WhileLoop(condition, body)
    

class ForLoopParser:
    def parse_for_loop(self):
        self.eat("FOR")
        
        self.eat("LPAREN")                     
        
        var = self.eat("IDENTIFIER")
        self.eat("COMMA")      

        self.eat("FROM")                    
        start = self.parse_expression()     

        self.eat("TO")                      
        end = self.parse_expression()       
        
        self.eat("RPAREN")
        
        self.eat("LBRACKET")                
        body = self.parse_block()

        return ForLoop(var, start, end, body)