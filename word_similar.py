from pyvi import ViTokenizer
from gensim.models.keyedvectors import KeyedVectors

class Word_Similar():
    def __init__(self, path_model="./word2vec/baomoi.window2.vn.model.bin", N=3, path_sw='vi_stopwords.txt'):
        self.model = KeyedVectors.load_word2vec_format(path_model, binary=True)
        self.numbe_top = N
        self.stopword = self.get_stopword(path_sw)

    def filter_stopwords(self, sentence):
        words = ViTokenizer.tokenize(sentence).split()
        w = []
        for word in words:
            if word not in self.stopword:
                w.append(word)
        return w

    def get_stopword(self, paths):
        stopword = []
        with open(paths, 'r') as files:
            for word in files:
                stopword.append(word.replace("\n", ''))
        return stopword

    def find_word_similar(self, sentence):
        words = self.filter_stopwords(sentence)
        word_similar = []
        for word in words:
            try:
                word_similar.append(self.model.wv.most_similar(positive=[word], topn=self.numbe_top))
            except:
                pass
        return word_similar

# ws = Word_Similar()

# print(ws.find_word_similar("bóng đá việt nam"))
    