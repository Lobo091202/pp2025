class Course:
    def __init__(self, cid, name, credit):
        self.__id = cid
        self.__name = name
        self.__credit = credit

    def get_id(self): return self.__id
    def get_name(self): return self.__name
    def get_credit(self): return self.__credit
