class F(object):
    SPACES = ('                                                \n'
              '                                                       '
             )

    @classmethod
    def format(cls, s, length):
        if not isinstance(s, str):
            s = str(s)
        slen = length - len(s)
        if slen > len(cls.SPACES):
            slen = len(cls.SPACES)
        if slen > 0:
            return cls.SPACES[:slen] + s
        else:
            return s
