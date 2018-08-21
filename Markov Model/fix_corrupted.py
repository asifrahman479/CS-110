import stdio
import sys
from markov_model import MarkovModel


# Takes an integer k (model order) and a string s (noisy message) as
# command-line arguments, reads the input text from standard input, and
# prints out the most likely original string.
def main():
    k = int(sys.argv[1])
    s = sys.argv[2]
    text = sys.stdin.read()
    model = MarkovModel(text, k)
    r = model.replace_unknown(s)
    for i in range(0, len(r)):
        if i == len(r) - 1:
            stdio.writeln(r[i])
        else:
            stdio.write(r[i])


if __name__ == '__main__':
    main()
