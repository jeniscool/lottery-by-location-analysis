
class City:

    ''' Constructor '''
    def __init__(self, city, state, area, avg_income, num_households):
        self.city = city
        self.state = state
        self.area = area
        self.avg_income = avg_income
        self.num_households = num_households


    ''' Returns the string representation of the object. '''
    def __repr__(self):
        return str(self)

    ''' Returns the string representation of the object. '''
    def __str__(self):
        return 'City(\''+self.city+'\',\''+self.state+'\','+str(self.area)+','+str(self.avg_income)+','+str(self.num_households)+')'

    ''' Implements equality comparison '''
    def __eq__(self, other):
        if self.state == other.state:
            if self.city == other.city:
                return True
        return False

    ''' Implements less than comparison to sort alphabetically'''
    def __lt__(self, other):

        if self.state < other.state:
            return True
        elif self.state > other.state:
            return False
        else:
            if self.city < other.city:
                return True
            else:
                return False

    ''' Implement an appropriate hash function for these objects '''
    def __hash__(self):
        return hash(repr(self)) # use string representation to hash
