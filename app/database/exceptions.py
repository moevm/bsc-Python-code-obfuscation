class ObjectIdError(KeyError):
    def __init__(self, msg, id):
        super(ObjectIdError, self).__init__(msg)

        self.id = id
