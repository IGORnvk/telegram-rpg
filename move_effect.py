class MoveEffect:
    def __init__(self, is_finished):
        self.is_finished = is_finished


class AttackEffect(MoveEffect):
    def __init__(self, damage, is_finished):
        super().__init__(is_finished)
        self.damage = damage


class IncreasePowerEffect(MoveEffect):
    def __init__(self, value, is_finished):
        super().__init__(is_finished)
        self.value = value


class IncreaseDefenseEffect(MoveEffect):
    def __init__(self, value, is_finished):
        super().__init__(is_finished)
        self.value = value


class IncreaseHealthEffect(MoveEffect):
    def __init__(self, value, is_finished):
        super().__init__(is_finished)
        self.value = value


class IncreaseManaEffect(MoveEffect):
    def __init__(self, value, is_finished):
        super().__init__(is_finished)
        self.value = value
