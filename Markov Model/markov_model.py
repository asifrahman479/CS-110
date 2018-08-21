"""
markov_model.py

A data type that represents a Markov model of order k from a given text string.
"""

import stdio
import stdrandom
import sys


class MarkovModel(object):
    """
    Represents a Markov model of order k from a given text string.
    """

    def __init__(self, text, k):
        """
        Creates a Markov model of order k from given text. Assumes that text
        has length at least k.
        """

        self._k = k
        self._st = {}
        circ_text = text + text[:k]
        for i in range(len(circ_text) - k):
            kgram = circ_text[i:i + k]
            next_char = circ_text[i + k]
            self._st.setdefault(kgram, {})
            self._st[kgram].setdefault(next_char, 0)
            self._st[kgram][next_char] += 1

    def order(self):
        """
        Returns order k of Markov model.
        """

        return k

    def kgram_freq(self, kgram):
        """
        Returns number of occurrences of kgram in text. Raises an error if
        kgram is not of length k.
        """

        if self._k != len(kgram):
            raise ValueError('kgram ' + kgram + ' not of length ' +
                             str(self._k))
        if kgram not in self._st:
            return 0
        else:
            kgram_freq = self._st[kgram].values()
            return sum(kgram_freq)

    def char_freq(self, kgram, c):
        """
        Returns number of times character c follows kgram. Raises an error if
        kgram is not of length k.
        """

        if self._k != len(kgram):
            raise ValueError('kgram ' + kgram + ' not of length ' +
                             str(self._k))
        else:
            if c not in self._st[kgram]:
                return 0
            else:
                freq = self._st[kgram][c]
                return freq

    def rand(self, kgram):
        """
        Returns a random character following kgram. Raises an error if kgram
        is not of length k or if kgram is unknown.
        """

        if self._k != len(kgram):
            raise ValueError('kgram ' + kgram + ' not of length ' +
                             str(self._k))
        if kgram not in self._st:
            raise ValueError('Unknown kgram ' + kgram)

        k = self._st[kgram].keys()
        v = self._st[kgram].values()
        d = stdrandom.discrete(v)
        return k[d]

    def gen(self, kgram, T):
        """
        Generates and returns a string of length T by simulating a trajectory
        through the correspondng Markov chain. The first k characters of the
        generated string is the argument kgram. Assumes that T is at least k.
        """

        text = kgram
        while len(text) - T != 0:
            n = self.rand(kgram)
            text += n
            kgram = kgram[1:] + n
        return text

    def replace_unknown(self, corrupted):
        """
        Replaces unknown characters (~) in corrupted with most probable
        characters, and returns that string.
        """

        # Given a list a, argmax returns the index of the maximum element in a.
        def argmax(a):
            return a.index(max(a))

        original = []
        for i in range(len(corrupted)):
            if corrupted[i] == '~':
                a = i - self._k
                kgram_before = corrupted[a:i]
                kgram_after = corrupted[i + 1: self._k + i + 1]
                char_after = self._st[kgram_before].keys()
                probs = []
                for v in char_after:
                    context = kgram_before + v + kgram_after
                    p = 1.0
                    for i in range(self._k + 1):
                        kgram = context[i:self._k + i]
                        char = context[i + self._k]
                        if (kgram not in self._st\
                            or char not in self._st[kgram]):
                            p = 0
                            break
                        else:
                            q = self.char_freq(kgram, char) / float(self.kgram_freq(kgram))
                            p *= q
                    probs += [p]
                original += char_after[argmax(probs)]
            else:
                original += corrupted[i]
        return original


def _main():
    """
    Test client [DO NOT EDIT].
    """

    text, k = sys.argv[1], int(sys.argv[2])
    model = MarkovModel(text, k)
    a = []
    while not stdio.isEmpty():
        kgram = stdio.readString()
        char = stdio.readString()
        a.append((kgram.replace("-", " "), char.replace("-", " ")))
    for kgram, char in a:
        if char == ' ':
            stdio.writef('freq(%s) = %s\n', kgram, model.kgram_freq(kgram))
        else:
            stdio.writef('freq(%s, %s) = %s\n', kgram, char,
                         model.char_freq(kgram, char))

if __name__ == '__main__':
    _main()
