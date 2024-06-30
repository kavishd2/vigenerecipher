def encode(message, key):
    code = ""
    count = 0
    for i in message:
        if 65 <= ord(i) <= 90:
            code += chr((ord(i) + ord(key[count % len(key)])) % 26 + 65)
        elif 97 <= ord(i) <= 122:
            code += chr((ord(i) + ord(key[count % len(key)]) - 6) % 26 + 65)
        if 65 <= ord(i) <= 90 or 97 <= ord(i) <= 122:
            count += 1
            if count % 5 == 0:
                code += " "
    return code


def decode(string):
    max = 0
    clean = ""
    for i in string:
        if 65 <= ord(i) <= 90:
            clean += i
    strings = []
    letters = []
    for l in range(1, min(len(clean) // 15 + 1, 10)):  # Different lengths of key
        # Creates strings
        strings.append([])
        letters.append([])
        for i in range(l):
            strings[l - 1].append("")
        for i in range(len(clean)):
            strings[l - 1][i % l] += clean[i]
        avg_index = 0
        for i in range(l):
            # Counts number of letters
            letters[l - 1].append([])
            for j in range(26):
                letters[l - 1][i].append(0)
            for j in strings[l - 1][i]:
                letters[l - 1][i][ord(j) - 65] += 1
            # Calculates index of coincidence
            index = 0
            for j in range(26):
                index += letters[l - 1][i][j] * (letters[l - 1][i][j] - 1)
            index /= (len(strings[l - 1][i]) * (len(strings[l - 1][i]) - 1))
            avg_index = (avg_index * i + index) / (i + 1)
        if max < avg_index:
            max = avg_index
            length = l

    # Compute mutual index of coincidence
    for l in range(length):
        dist.append(0)
        edges.append([[] for j in range(length)])
    for l in range(length):
        edges[l][l].append(0)
    for l in range(length):
        for i in range(l + 1, length):
            max = []
            for k in range(26):
                index = 0
                for j in range(26):
                    index += letters[length - 1][l][j] * letters[length - 1][i][(j + k) % 26]
                index /= (len(strings[length - 1][l]) * len(strings[length - 1][i]))
                max.append(Shift(k, index))
            max.sort(reverse=True)
            edges[l][i].append(max[0].shift)
            edges[i][l].append(-max[0].shift%26)
            edges[l][i].append(max[1].shift)
            edges[i][l].append(-max[1].shift%26)
            if length < 7:
                edges[l][i].append(max[2].shift)
                edges[i][l].append(-max[2].shift % 26)
    for l in range(length):
        gen(0, l)

    # Finds most likely shift of key by telling gibberish from english using proportions of letters in the language
    prop = [.08497, .02072, .04539, .03384, .11161, .01812, .02471, .03003, .07545, .00197, .01102, .05489, .03013, .06654, .07164, .03167, .00196, .07581, .05735, .06951, .03631, .01007, .0129, .0029, .01778, .00272]
    max = 0
    key = ""
    shift = 0
    for k in keys:
        shifts = []
        for i in k:
            shifts.append(ord(i)-65)
        letter = []
        for i in range(26):
            letter.append(0)
            for l in range(length):
                letter[i] += letters[length-1][l][(i+shifts[l])%26]
        for i in range(26):
            index = 0
            for j in range(26):
                index += letter[(j+i)%26]*prop[j]
            if max < index:
                max = index
                key = k
                shift = i
    message = ""
    for i in range(len(clean)):
        message += chr((ord(clean[i]) - ord(key[i%length]) - shift)%26+65)
    return sentence_space(message)

# Creates possible keys recursively by fixing a base letter
def gen(index, base):
    if index == len(dist):
        key = ""
        for l in dist:
            key += chr(l+65)
        keys.add(key)
    else:
        if index == 0:
            for i in edges[0][base]:
                dist[base] = i
                gen(index+1,base)
                dist[base] = 0
        else:
            for i in edges[base][index]:
                dist[index] = (dist[base] + i) % 26
                gen(index + 1, base)
                dist[base] = 0

# Adds spaces to sentence
def sentence_space(string):
    for i in range(len(string)):
        done.append(False)
        previous.append([])
    word_splitter(string, 0)
    i = len(string)-1
    sentence = ""
    while i != -1:
        sentence = string[previous[i][0]:i+1] + " " + sentence
        i = previous[i][0] - 1
    return sentence

# Finds words from a starting index to recursively build sentence
def word_splitter(string, start):
    i = start
    current = trie.root
    while i < len(string) and current.child[ord(string[i])-65] != None:
        current = current.child[ord(string[i])-65]
        if current.end:
            previous[i].insert(0, start)
            if not done[i]:
                done[i] = True
                word_splitter(string, i+1)
        i += 1


# Used to find most likely shifts for each permutation
class Shift(object):
    def __init__(self, shift, index):
        self.shift = shift
        self.index = index

    def __lt__(self, other):
        return self.index < other.index

class Node(object):
    def __init__(self, end=False):
        self.child = [None] * 26
        self.end = end


class Trie(object):
    def __init__(self):
        self.root = Node()

    def add(self, word):
        current = self.root
        for i in word:
            if current.child[ord(i)-97] == None:
                current.child[ord(i)-97] = Node()
            current = current.child[ord(i)-97]
        current.end = True

    def string_help(self, node, string):
        if node.end:
            print(string)
        for i in range(26):
            if node.child[i] != None:
                self.string_help(node.child[i], string + chr(i+65))


dist = []
edges = []
keys = set()
trie = Trie()
file = open("words.txt")
while True:
    content = file.readline().strip()
    if not content:
        break
    trie.add(content)
file.close()
done = []
previous = []

# Test cases
code = encode("The eyes of texas are upon you, all the live long day. The eyes of texas are upon you, you cannot get away. Do not think you can escape them by night or early in the morn. The eyes of texas are upon you til Gabriel blows his horn", "LONGHORN")
print(code)
print(decode(code))
#print(decode("ISATA IFXXP FIBGP PYHGP SBXMO KMOXL FFPVI IWIVZ PMUXP FGPPY HBPAB CWTMR HWEMS YE"))