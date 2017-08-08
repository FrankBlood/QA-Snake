#coding:utf8

import jieba
import jieba.posseg as pseg
import os,sys


def jieba_initialize():
    '''initialize jieba Segment
    初始化结巴分词
    :return: None
    '''
    jieba.load_userdict(os.path.dirname(os.path.split(os.path.realpath(__file__))[0])+'/resources/QAattrdic.txt')
    jieba.initialize()


def wordSegment(text):
    '''Segment words by jieba
    通过结巴进行分词
    :param text:
    :return: 以空格为间隔的词序列
    '''
    text = text.strip()
    seg_list = jieba.cut(text)
    result = " ".join(seg_list)
    return result


def postag(text):
    '''POS Tagging
    词性标注
    :param text:
    :return: 词性标注结果的迭代器
    '''
    words = pseg.cut(text)
    # for w in words:
    #     print w.word, w.flag
    return words


def xiaohuangji_textprocess(fr_path,fw_path):
    '''proecss xiaohuangji corpus
    处理小黄鸡语料库
    :param fr_path:
    :param fw_path:
    :return: 把原来的数据转化为问题答案数据对
    '''
    fr = open(fr_path,'r')
    fw = open(fw_path,'a')
    line = fr.readline()
    i = 0

    while line:
        if line[0] == 'E':
            question = fr.readline()[2:].strip()
            answer = fr.readline()[2:]
            print question
            print answer
            if len(question)<20 and len(answer)<30:
                i +=1
                qa_pair = question+":::"+answer
                fw.write(qa_pair)
        line = fr.readline()

    fw.close()
    fr.close()
    print 'Finished'


def tp2(fr_path,fw_path):
    '''q:::a text processing

    :param fr_path:
    :param fw_path:
    :return: 对问题和答案对进行处理
    '''
    fr = open(fr_path,'r')
    fw = open(fw_path,'a')
    line = fr.readline()
    while line:
        flag = 0
        words = pseg.cut(line)
        for w in words:
            print w.word, w.flag
            if w.flag == 'nr':
                flag = 1
        if flag == 0:
            fw.write(line)
        line = fr.readline()

    fw.close()
    fr.close()
    print 'Finished'


def load_baikeattr_name(attrdic):
    '''Load baike attributi name

    :param attrdic:
    :return: 获取百科数据
    '''
    fr = open(attrdic,'r')
    attr = []
    line = fr.readline()
    while line:
        attr.append(line.strip())
        line = fr.readline()
    fr.close()
    return attr


def load_synonyms_word_inattr(word,synsdic,attr):
    ''' Synonyms Analysis,return word in baike attr

    :param word: 原始词
    :param synsdic: 同义词典
    :param attr: 属性
    :return: 不知道是干啥的。。
    '''
    fr = open(synsdic,'r')
    tar_word = ''
    line = fr.readline().strip()
    while line:
        words = line.split(" ")
        if word in words:
            for w in words:
                if w in attr:
                  tar_word = w
                  break
        if tar_word != '':
            break
        line = fr.readline()
    fr.close()
    if tar_word == '':
        tar_word = 'Empty'
    return tar_word

if __name__ == '__main__':
    pass
    # tp2('./corpus/xiaohuangji50w_clean2.txt','./corpus/xiaohuangji50w_clean3.txt')
    # postag("华中科技大学校长是谁？")
