import traceback
import argparse


class Evaluate():
    def readFile(self, file_name):
        # stores solved equations
        solved = {}
        # stores unsolved equations
        unSolved = {}
        try:
            infile = open(file_name, "r")
            # goes through all lines in the file
            for line in infile:
                # Ignore empty lines in the file
                if not line.strip():
                    continue
                else:
                    # split each equation by '=' to separate LHS&RHS
                    equation = line.strip().split('=')
                    lhs = equation[0].strip()
                    # strip spaces in rhs and split by '+'
                    rhs = equation[1].strip().split('+')
                    # method checks if the equations are already solved
                    modified_rhs, sum = self.check_solved(rhs, solved)
                    if sum != -1:
                        solved[lhs] = sum
                    else:
                        unSolved[lhs] = modified_rhs
            # finally solve all the equations iteratively
            solved_equations = self.equation_solver(solved, unSolved)
            # sort the dictionary alphabetically
            keylist = sorted(solved_equations.keys())
            for key in keylist:
                print "%s = %s" % (key, solved_equations[key])
        except Exception:
            print "File not exists"
            traceback.print_exc()

    def equation_solver(self, solved, unsolved):
        while unsolved:
            for equations in unsolved:
                for variable in unsolved[equations]:
                    # checks if the variable is int/string
                    if isinstance(variable, str):
                        # checks if the variable is already in solved
                        if variable in solved:
                            index = unsolved[equations].index(variable)
                            unsolved[equations][index] = solved[variable]
            modified_rhs, sum = self.check_solved(unsolved[equations], solved)
            if sum != -1:
                solved[equations] = sum
                unsolved.pop(equations)
            else:
                unsolved[equations] = modified_rhs
        return solved

    def check_solved(self, rhs, solved):
        isSolved = True
        sum = 0
        modified_rhs = []
        for each_var in rhs:
            if each_var in solved:
                each_var = solved[each_var]
            if not (self.isInt(each_var)):
                isSolved = False
                modified_rhs.append(each_var.strip())
            else:
                sum += int(each_var)
        if isSolved:
            return modified_rhs, sum
        modified_rhs.append(sum)
        return modified_rhs, -1

    def isInt(self, var):
        try:
            int(var)
            return True
        except ValueError:
            return False


def main():
    parser = argparse.ArgumentParser()
    # add an argument for file input
    parser.add_argument('file', help='path to equations file', nargs='+')
    args = parser.parse_args()
    file_name = args.file[0]
    Evaluate().readFile(file_name)


if __name__ == '__main__':
    main()
