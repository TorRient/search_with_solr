from pyvi import ViTokenizer
from gensim.models.keyedvectors import KeyedVectors

class Word_Similar():
    def __init__(self, path_model="./word2vec/baomoi.window2.vn.model.bin", N=3):
        self.model = KeyedVectors.load_word2vec_format(path_model, binary=True)
        self.numbe_top = N
    def find_word_similar(self, word):
        word_similar = self.model.wv.most_similar(positive=[word], topn=self.numbe_top)
        return word_similar

# ws = Word_Similar()

# print(ws.find_word_similar("Hồ_cHí_minh"))
    