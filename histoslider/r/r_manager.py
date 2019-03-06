from rpy2 import robjects


class RManager:
    def __init__(self):
        result = robjects.r('''
                # create a function `f`
                f <- function(r, verbose=FALSE) {
                    if (verbose) {
                        cat("I am calling f().\n")
                    }
                    2 * pi * r
                }
                # call the function `f` with argument value 3
                f(3, TRUE)
                ''')
        print(result)
