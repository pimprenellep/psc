
class StanceGraph :
    def __init__(self, route) :
        self.route = route

        # Code de génération du graphe
        ###
        print("Building stance graph")

        Lpos = []
        G = []

        self.stances = Lpos
        self.nextStances = G

    def getRoute(self):
        return self.route

    
    def getGraphRep(self):
        return (self.stances, self.nextStances)
        

