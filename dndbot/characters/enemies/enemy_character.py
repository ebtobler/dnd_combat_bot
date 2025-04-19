from collections.abc import MutableMapping


class EnemyCharacter(MutableMapping):

    def __init__(self, stats: dict):
        self.stats = stats

    def __setitem__(self, k, v):
        self.stats[k] = v

    def __delitem__(self, v):
        del self.stats[v]

    def __getitem__(self, k):
        return self.stats[k]

    def __len__(self) -> int:
        return len(self.stats)

    def __iter__(self):
        return iter(self.stats)
