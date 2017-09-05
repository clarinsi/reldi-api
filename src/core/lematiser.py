# -*- coding: utf-8 -*-
import cPickle as pickle
from train_lemmatiser import extract_features_lemma


class Lematiser(object):
    '''Class segmenter'''

    def __init__(self, lang, segmenter, tagger):
        self.lang = lang
        self.lemmatiser = {
            'model': pickle.load(open('assets/' + lang + '.lexicon.guesser')),
            'lexicon': pickle.load(open('assets/' + lang + '.lexicon'))
        }
        self.segmenter = segmenter
        self.tagger = tagger

    def apply_rule(self, token, rule, msd):
        rule=list(eval(rule))
        if msd:
            if msd[:2] == 'Np':
                lemma = token
            else:
                lemma = token.lower()
        else:
            lemma=token.lower()

        rule[2]=len(token)-rule[2]
        lemma=rule[1]+lemma[rule[0]:rule[2]]+rule[3]
        return lemma

    def getLemma(self, token, msd):
        """
        Returns the lemma for a specific token

        :param token: The token to be lemmatized
        :param mdf: The msd/tag of the token
        :return: returns lemma for token
        """
        lexicon = self.lemmatiser['lexicon']
        key = token.lower() + '_' + msd
        if key in lexicon:
            return lexicon[key][0].decode('utf8')
        if msd[:2] != 'Np':
            for i in range(len(msd)):
                for key in lexicon.keys(key[:-(i + 1)]):
                    return lexicon[key][0].decode('utf8')

        return self.guessLemma(token, msd)

    def guessLemma(self, token, msd):
        """
        Predicts the lemma for a specific token
        """
        model = self.lemmatiser['model']
        if msd not in model:
            return token
        else:
            return self.apply_rule(token, model[msd].predict(extract_features_lemma(token))[0], msd)

    def lemmatise(self, sentence, vert=False):
        """
        Lemmatises a sentence
        """
        return [[(a, c) for a, b, c in sent] for sent in self.tagLemmatise(sentence, vert)]

    def tagLemmatise(self, sentence, vert=False):
        """
        Tags and lemmatises a sentence
        """
        taggedOutput = self.tagger.tag(sentence)
        output = []
        for s in taggedOutput:
            output.append([(t[0], t[1], self.getLemma(t[0][0], t[1])) for t in s])
        return output
