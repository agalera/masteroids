class casilla:
    def __init__ (self, tile, objeto_arma = None):
        self.tile = tile
        self.objeto_arma = objeto_arma
    def get_tile(self):
        if self.objeto_arma == None:
            return self.tile
        else:
            return self.objeto_arma.get_id()
    def get_object(self):
        return self.objeto_arma
    def set_tile(self, tile, objeto_arma = None):
        self.tile = tile
        self.objeto_arma = objeto_arma
#    def block(self):
#        if self.get_tile() == -1:
#            return True
#        else:
#            return False
