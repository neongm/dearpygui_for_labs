import numpy as np

class LS():
    def __init__(self, X_matrix: list, Y_matrix: list):
        self.X_matrix = X_matrix
        self.Y_matrix = Y_matrix
        self._to_npmatrix()

    def _to_npmatrix(self):
        for row in self.X_matrix: row.insert(0, 1) # inserts 1 at idx 0 for every row

        self.X = np.matrix(self.X_matrix)
        self.Y = np.matrix(self.Y_matrix).transpose()
        self.X_dimentions = self.X.shape

        print(f'X:\n{self.X}', f'Y:\n{self.Y}', sep='\n')

    def solve_numpy(self):
        x = np.linalg.lstsq(self.Y, self.X, rcond=None)[0]
        res = [x.item(i) for i in range(x.shape[1])]
        return res

    def solve_myown(self):
        Xt = self.X.transpose()
        print(f"Xt:\n{Xt}")
        X = self.X
        Y = self.Y

        XtX = Xt.dot(X)
        print(f"XtX:\n{XtX}")

        XtY = Xt.dot(Y)
        print(f"XtY:\n{XtY}")

        XtXi = np.linalg.inv(XtX)
        print(f"XtXi:\n{XtXi}")

        s = XtXi.dot(XtY)

        print(f"Result Vector:\n{s}")

        res = [s.item(i) for i in range(s.shape[0])]
        return res


def test():
    Xm = [
        [0,  2, 4],
        [6,  12, 5],
        [8, 16, 125],
        [6, 12, 23],
        [4,  8, 23]
    ]
    C = [0, 2, 3, 4]
    Ym = [
        sum([y[i] for i in range(len(Xm[0]))]) for y in Xm
    ]
    # Ym = [
    #     [2, 3, 4, 3, 2]
    # ]

    solver = LS(Xm, Ym)
    print(solver.solve_myown())





if __name__ == "__main__": test()
