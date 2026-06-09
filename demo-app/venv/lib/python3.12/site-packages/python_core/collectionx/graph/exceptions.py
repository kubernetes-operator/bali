

class GraphExceptions(Exception):
    pass

class VertexNotFoundError(GraphExceptions):
    def __init__(self, message=""):
        self.message = message