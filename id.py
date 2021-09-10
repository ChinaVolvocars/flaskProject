class IdCard:
    def __init__(self, name, gender, ethnic, born, address, id_number):
        self.ethnic = ethnic
        self.gender = gender
        self.name = name
        self.born = born
        self.address = address
        self.id_number = id_number

    def obj_2_json(self):
        return {
            "name": self.name,
            "gender": self.gender,
            "ethnic": self.ethnic,
            "born": self.born,
            "address": self.address,
            "id_number": self.id_number
        }
