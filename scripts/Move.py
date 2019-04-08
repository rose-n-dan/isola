class Move:
    def __init__(self, start_row, start_col, end_row, end_col):
        if not (0 <= start_row < 8) or \
           not (0 <= start_col < 8) or \
           not (0 <= end_row < 8) or \
           not (0 <= end_col < 8):
            raise IOError('Move starting or ending point does not fit into the board')
        self.start_row = start_row
        self.start_col = start_col
        self.end_row = end_row
        self.end_col = end_col

    def __repr__(self):
        return '[{}, {}] ---> [{}, {}]'.format(self.start_row, self.start_col,
                                               self.end_row, self.end_col)

    def undo(self):
        self.start_col, self.end_col = self.end_col, self.start_col
        self.start_row, self.end_row = self.end_row, self.start_row
