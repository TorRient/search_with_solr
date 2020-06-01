from pyvi import ViTokenizer
from gensim.models.keyedvectors import KeyedVectors

class Word_Similar():
    def __init__(self, path_model="./word2vec/baomoi.window2.vn.model.bin", N=3, path_sw='vi_stopwords.txt'):
        self.model = KeyedVectors.load_word2vec_format(path_model, binary=True)
        self.number_top = N
        self.stopword = self.get_stopword(path_sw)

    def filter_stopwords(self, sentence, stop=True):
        words = ViTokenizer.tokenize(sentence).split()
        if stop:
            w = []
            for word in words:
                if word not in self.stopword:
                    w.append(word)
            return w
        return words

    def get_stopword(self, paths):
        stopword = []
        with open(paths, 'r') as files:
            for word in files:
                stopword.append(word.replace("\n", ''))
        return stopword

    def find_word_similar(self, sentence):
        sentence = sentence.lower()
        words = self.filter_stopwords(sentence, stop=False)
        word_similar = []
        for word in words:
            word_similar.append([(word,1.0)])
            try:
                word_similar.append(self.model.wv.most_similar(positive=[word], topn=self.number_top))
            except:
                pass
        text = ''
        # print(word_similar)
        for words in word_similar:
            for word in words:
                if word[1] > 0.7:
                    text += "'" + word[0] + "' "
        
        return text[:-1]

# ws = Word_Similar()

# print(ws.find_word_similar("Phòng"))
    