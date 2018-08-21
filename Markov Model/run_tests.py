import datetime, os, signal, subprocess, sys, time, unittest

def run(command, stdin = None, timeout = 30):
    """
    Runs the specified command using specified standard input (if any) and
    returns the output on success. If the command doesn't return within the
    specified time (in seconds), "__TIMEOUT__" is returned.
    """

    start = datetime.datetime.now()
    process = subprocess.Popen(command, # command.split()
                               stdin = subprocess.PIPE, 
                               stdout = subprocess.PIPE,
                               stderr = subprocess.STDOUT)
    if not stdin is None:
        process.stdin.write(stdin)
        process.stdin.close()
    while process.poll() is None:
        time.sleep(0.1)
        now = datetime.datetime.now()
        if (now - start).seconds > timeout:
            os.kill(process.pid, signal.SIGKILL)
            os.waitpid(-1, os.WNOHANG)
            return "__TIMEOUT__"
    return process.stdout.read()

class Problem1(unittest.TestCase):

    def test1(self):
        command = ["python", "markov_model.py", "banana", "2"]
        sought = """freq(an, a) = 2
freq(na, b) = 1
freq(na, a) = 0
freq(na) = 2
"""
        got = run(command, "an a na b na a na -")
        self.assertNotEquals(got, "__TIMEOUT__")
        self.assertEquals(got, sought)

    def test2(self):
        command = ["python", "markov_model.py", "gagggagaggcgagaaa", "2"]
        sought = """freq(aa, a) = 1
freq(ga, g) = 4
freq(gg, c) = 1
freq(ag) = 5
freq(cg) = 1
freq(gc) = 1
"""
        got = run(command, "aa a ga g gg c ag - cg - gc -")
        self.assertNotEquals(got, "__TIMEOUT__")
        self.assertEquals(got, sought)
        
class Problem2(unittest.TestCase):

    def test1(self):
        text, k, l = open("data/input17.txt", "r").read(), 2, 50
        command = ["python", "text_generator.py", str(k), str(l)]
        got = run(command, text)
        self.assertNotEquals(got, "__TIMEOUT__")
        self.assertTrue(len(got) == l + 1 and got.startswith(text[:k]))

class Problem3(unittest.TestCase):

    def test1(self):
        command = ["python", "fix_corrupted.py", "4", "it w~s th~ bes~ of tim~s, i~ was ~he wo~st of~times."]
        sought = """it was the best of times, it was the worst of times.
"""
        got = run(command, open("data/obama.txt", "r").read())
        self.assertNotEquals(got, "__TIMEOUT__")
        self.assertEquals(got, sought)
        
    def test2(self):
        command = ["python", "fix_corrupted.py", "2", "it w~s th~ bes~ of tim~s, i~ was ~he wo~st of~times."]
        sought = """it was the best of times, is was the worst of times.
"""
        got = run(command, open("data/obama.txt", "r").read())
        self.assertNotEquals(got, "__TIMEOUT__")
        self.assertEquals(got, sought)

if __name__ == "__main__":
    unittest.main()
