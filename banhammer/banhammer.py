class Banhammer():

    def __init__(self):
        self.subreddits = list()

    def add_subreddits(self, *subs):
        for sub in subs:
            print(sub)


bh = Banhammer()
