import sys
import re
import random


def tokenize(text):
    """Takes plain text and transforms it into tokens (list of words and punctuation)"""
    text = text.lower()
    sents = re.split('\\.|\\?|!', text)  # splits text along sentences
    sents = [s.strip() for s in sents]  # gets rid of leading/trailing whitespace
    tokens = []
    for s in sents:
        tokens.append(re.findall(r"[\w']+|[,;]", s))
    return tokens


def generate_ngrams(tokens, n):
    """Takes tokens and n, generating ngrams"""
    tokens = [x for x in tokens if len(x) >= n]  # gets rid of sentences smaller than n
    output = []
    for t in tokens:

        # cycles through every sentence
        for i in range(len(t) - n + 1):
            # <start> padding
            if i == 0:
                z = 1
                for j in range(n - 1, 0, -1):
                    add = []
                    firstn = t[:n - 1]
                    for k in range(j):
                        add.append('<start>')
                    for tmp in range(z):
                        add.append(firstn[tmp])
                    z += 1
                    output.append(add)

            # bulk of ngram processing
            output.append(t[i:i + n])

            # <end> padding
            if i == len(t) - n:
                lastn = t[-n + 1:]
                add = []
                for k in range(n - 1):
                    add.append(lastn[k])
                add.append('<end>')
                output.append(add)
    output = [tuple(l) for l in output]
    return output


class Model:

    def __init__(self, n):
        self.n = n
        self.prev = ()
        self.count = {}

    def populate(self, ngrams):
        """creates dictionary of ngrams and their frequency"""
        for ngram in ngrams:
            if ngram in self.count:
                self.count[ngram] += 1.0
            else:
                self.count[ngram] = 1.0

    def find_word(self):
        """find a word given previous n-1 words, as saved in the model"""
        diction = self.count
        coll = []

        # searches through dictionary to find all occurrences of the previous n-1 values
        for d in diction:
            bool = True
            for i in range(n - 1):
                if d[i] == self.prev[i]:
                    pass
                else:
                    bool = False
                    break
            if bool:
                coll.append(d)
        diction_subset = {key: diction[key] for key in coll}
        tot_freq = 0
        for key in diction_subset:
            tot_freq += diction_subset[key]  # find total frequency for previous n-1 words
        rand = random.randint(0, tot_freq)
        word = ""

        # generate a random number between 0 and total frequency of n-1 words, then use that number to search
        # dictionary until it lands on the word indicated by the number (I recognize this isn't normalized at all
        # but it does still work just fine)
        for key in diction_subset:
            rand -= diction_subset[key]
            if rand <= 0:
                word = key[-1]  # as soon as the word associated with the random number is found, stop looking
                break
        return word

    def generate_sentences(self, m):
        """generates m random sentences"""
        for _ in range(m):
            end = False
            sent = ""

            # for the very beginning of the sentence, it'll search for a new word with n-1 <start> tags
            self.prev = ('<start>',) * (self.n - 1)
            while not end:  # while an <end> tag has not been reached
                new_word = self.find_word()  # gets a new word based on the previous n-1 words
                if new_word == '<end>':
                    end = True
                else:  # updates previous n-1 words
                    tmp_tup = self.prev[1:]
                    l = []
                    for e in tmp_tup:
                        l.append(e)
                    l.append(new_word)
                    sent += new_word
                    sent += " "
                    self.prev = tuple(l)

            print(sent + ".")


if __name__ == '__main__':
    # starting comment
    print("Cannon West, 3/1/21")
    print("Welcome to Cannon West's Ngram model. The goal of this program is to generate sentences word by word using "
          "only the previous words for context,\nreferencing a provided text such as the works of William Shakespeare "
          "or Sir Arthur Conan Doyle. The parameters include the n value,\nwhich represents how much context we should "
          "be referencing on our text, the number or sentences to be generated m, and the text files to reference.\n("
          "for example, ngram.py 3 10 sherlock.txt shakespeare.txt  <-- this will generate 10 sentences per text with "
          "n=3")
    print()

    print("Example: given the parameters n=3 and text=sherlock.txt, the program generated the following sentences:")
    print("she knows that the king is capable of heroic self sacrifice and that anything dishonourable would be "
          "repugnant to her .")
    print("let us follow it out to the southern suburb , but sat with his chin upon his hands and stared into the "
          "crackling fire .")
    print()

    print("The way my program works is by taking in files as plain text, generating ngrams, then using the frequency "
          "of each (n-1)gram against a randomly generated\nnumber between 0 and freq to determine what the new word "
          "should be. The program will then continue generating words until an <end> tag is reached.")
    print()

    print("PLEASE NOTE: The program only works with txt files in the UTF-8 format")
    print()

    # command line stuff
    n = int(sys.argv[1])
    m = int(sys.argv[2])
    txts = []
    for i in range(3, len(sys.argv)):
        txts.append(sys.argv[i])

    # creating data from files
    data = []
    for t in txts:
        with open(t, 'r', encoding='utf8') as file:
            data.append(file.read().replace('\n', ' '))

    for i in range(len(sys.argv) - 3):
        print("Text: ", txts[i])
        tokens = tokenize(data[i])
        ngrams = generate_ngrams(tokens, n)
        ng = Model(n)
        ng.populate(ngrams)
        ng.generate_sentences(m)
        print()

    print("all done!")
