class Solfege_Pattern:
    dic = dict()
    set_ = dict()

    def __init__(self, names):
        self.names = names
        for name in names:
            self.dic[self.__class__][name] = self
        self.set_[self.__class__].append(self)

    def getFirstName(self):
        return self.names[0]

    def getNames(self):
        return self.names
