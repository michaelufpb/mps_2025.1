from entity.lab import Lab

class Memento:
    def __init__(self, state):
        self.state = state

class LabOriginator:
    def __init__(self, lab: Lab):
        self.lab = lab

    def save(self) -> Memento:
        return Memento(self.lab.to_dict())

    def restore(self, memento: Memento):
        self.lab.__dict__.update(memento.state)