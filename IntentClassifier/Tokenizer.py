import jieba


class Tokenizer():
    @classmethod
    def set_dict(cls, path):
        jieba.set_dictionary(path)

    @classmethod
    def cut(cls, sentence):
        return list(jieba.cut(sentence))
