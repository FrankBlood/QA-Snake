# -*- coding:utf8 -*-

from __future__ import print_function
from pyltp import SentenceSplitter, Segmentor, Postagger, Parser, NamedEntityRecognizer, SementicRoleLabeller


class Semantic_Parser(object):
    def __init__(self):
        self.cws_model_path = '/home/irlab0/LTP/ltp-data/ltp_data/cws.model'
        self.pos_model_path = '/home/irlab0/LTP/ltp-data/ltp_data/pos.model'
        self.parser_model_path = '/home/irlab0/LTP/ltp-data/ltp_data/parser.model'
        self.ner_model_path = '/home/irlab0/LTP/ltp-data/ltp_data/ner.model'
        self.srl_model_path = '/home/irlab0/LTP/ltp-data/ltp_data/srl/'

    def load(self):
        self.segmentor = Segmentor()
        self.segmentor.load(self.cws_model_path)

        self.postagger = Postagger()
        self.postagger.load(self.pos_model_path)

        self.parser = Parser()
        self.parser.load(self.parser_model_path)

        self.recognizer = NamedEntityRecognizer()
        self.recognizer.load(self.ner_model_path)

        self.labeller = SementicRoleLabeller()
        self.labeller.load(self.srl_model_path)

    def release(self):
        self.segmentor.release()
        self.postagger.release()
        self.parser.release()
        self.recognizer.release()
        self.labeller.release()

    def get_cws(self, sentence):
        try:
            cws = self.segmentor.segment(sentence)
        except:
            cws = self.segmentor.segment(sentence.decode('utf8'))
        print(" ".join(cws))
        return cws

    def get_pos(self, cws):
        postags = self.postagger.postag(cws)
        print(" ".join(postags))
        return postags

    def get_arcs(self, cws, postags):
        arcs = self.parser.parse(cws, postags)
        label = " ".join("%s:%d:%s" % (word, arc.head, arc.relation) for word, arc in zip(cws, arcs))
        print(label)
        return arcs

    def get_role(self, cws, postags, arcs):
        netags = self.recognizer.recognize(cws, postags)
        roles = self.labeller.label(cws, postags, netags, arcs)
        for role in roles:
            print(role.index,
                  "".join(["%s:(%d,%d)" % (arg.name, arg.range.start, arg.range.end)
                           for arg in role.arguments]))

    def get_query(self, cws, arcs):
        '''
        对问句做句法分析后，提取其中的主干部分
        先取HED,然后分别取SBV和VOB

        :param cws:
        :param arcs:
        :return:
        '''
        words = [word for word in cws]
        head = [arc.head for arc in arcs]
        relation = [arc.relation for arc in arcs]
        print(words)
        print(head)
        print(relation)
        hed_index = index(head, 0)[0]+1
        import_index = index(head, hed_index)
        print(import_index)
        sbv = [words[i] for i in import_index if relation[i] == 'SBV']
        vob = [words[i] for i in import_index if relation[i] == 'VOB']
        print(''.join(sbv))
        print(''.join(vob))
        return ''.join(sbv), ''.join(vob)

def index(l, t):
    return [i for i, x in enumerate(l) if x == t]

def test_query():
    semantic_parser = Semantic_Parser()
    semantic_parser.load()
    sentence = "泰康总部在哪里？"
    cws = semantic_parser.get_cws(sentence)
    postags = semantic_parser.get_pos(cws)
    arcs = semantic_parser.get_arcs(cws, postags)
    head, relation = semantic_parser.get_query(cws, arcs)
    print(head, relation)
    semantic_parser.release()

def test_arcs():
    semantic_parser = Semantic_Parser()
    semantic_parser.load()
    sentence = "泰康总部在哪里？"
    cws = semantic_parser.get_cws(sentence)
    postags = semantic_parser.get_pos(cws)
    arcs = semantic_parser.get_arcs(cws, postags)
    semantic_parser.release()

def test_role():
    semantic_parser = Semantic_Parser()
    semantic_parser.load()
    sentence = "泰康总部在哪里？"
    cws = semantic_parser.get_cws(sentence)
    postags = semantic_parser.get_pos(cws)
    arcs = semantic_parser.get_arcs(cws, postags)
    role = semantic_parser.get_role(cws, postags, arcs)
    semantic_parser.release()

if __name__ == '__main__':
    # test_role()
    # test_arcs()
    test_query()