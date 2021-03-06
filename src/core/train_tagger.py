#!/usr/bin/python
#-*-coding:utf8-*-

import sys
import re
import codecs
import cPickle as pickle
import pycrfsuite

sys.stdout = codecs.getwriter('utf8')(sys.stdout)

def conll_iter(stream):
  sent=[]
  for line in stream:
    if line.strip()=='':
      yield sent
      sent=[]
    else:
      sent.append(line.decode('utf8').strip().split('\t'))

def packed_shape(token,index):
  packed=''
  for char in token:
    if char.isupper():
      packed+='u'
    elif char.islower():
      packed+='l'
    elif char.isdigit():
      packed+='d'
    else:
      packed+='x'
  if index==0:
    packed+='_START'
  return re.sub(r'(.)\1{2,}',r'\1\1',packed)

def islcase(token):
  return token.lower()==token

def isnum(token):
  import re
  return re.search(r'\d',token)!=None

def transnum(token):
  import re
  return re.sub(r'\d','D',token)

def wpos(sent,index):
  if index>=0 and index<len(sent):
    return transnum(sent[index].lower())

def wsuf(token,length):
  if token==None:
    return
  if len(token)>length:
    token=transnum(token.lower())
    return token[-length:]

def getpos(tag):
  if tag not in gram_feat:
    return None
  return gram_feat[tag].get('pos')

def getgender(tag):
  if tag not in gram_feat:
    return None
  return gram_feat[tag].get('Gender')

def getnumber(tag):
  if tag not in gram_feat:
    return None
  return gram_feat[tag].get('Number')

def getcase(tag):
  if tag not in gram_feat:
    return None
  return gram_feat[tag].get('Case')

def search_trie(token,trie,iscomplete=False):
  token='_'+token
  for i in range(len(token)):
    if token[-len(token)+i:] in trie:
      if iscomplete:
        if i==0:
          return (trie[token[-len(token)+i:]],True)
        else:
          return (trie[token[-len(token)+i:]],False)
      return trie[token[-len(token)+i:]]

def decode(s):  
  return ''.join(s).strip('0')

def reverse(s):
  t=''
  for u in s:
    t=u+t
  return t

def search_marisa(token,trie,iscomplete=False):
  token=reverse(u'_'+token)
  if token in trie:
    return [decode(e) for e in trie[token]]
  else:
    prefixes=trie.prefixes(token)
    if len(prefixes)>0:
      return [decode(e) for e in trie[sorted([(len(e),e) for e in prefixes],reverse=True)[0][1]]]

def escape_colon(text):
  return text.replace('\\','\\\\').replace(':','\\:')

def extract_features_msd(sent,trie,search=search_marisa): #originally "combined2", relates to the model named "lexicon"
  msds_sent=[]
  for token in sent:
    msds_sent.append(search(token.lower(),trie))
  features=[]
  for index,token in enumerate(sent):
    tfeat=[]
    tfeat.append('w[0]='+wpos(sent,index))
    tfeat.append('packed_shape='+packed_shape(token,index))
    for i in range(3): #w[-1] w[1]
      if wpos(sent,index-i-1)!=None:
        tfeat.append('w['+str(-i-1)+']='+wpos(sent,index-i-1))
      if wpos(sent,index+i+1)!=None:
        tfeat.append('w['+str(i+1)+']='+wpos(sent,index+i+1))
    for i in range(4): #w[0] suffix
      if wsuf(token,i+1)!=None:
        tfeat.append('s['+str(i+1)+']='+wsuf(token,i+1))
    if msds_sent[index]!=None:
      for msd in msds_sent[index]:
        tfeat.append('msd='+msd)
    for i in range(2):
      if wpos(sent,index-i-1)!=None:
        msds=msds_sent[index-i-1]
        if msds!=None:
          for msd in msds:
            tfeat.append('msd[-'+str(i+1)+']='+msd)#+':'+str(float(msds[msd])/sum(msds.values())))
      if wpos(sent,index+i+1)!=None:
        msds=msds_sent[index+i+1]
        if msds!=None:
          for msd in msds:
            tfeat.append('msd['+str(i+1)+']='+msd)#+':'+str(float(msds[msd])/sum(msds.values())))
    if index==0:
      tfeat.append('__BOS__')
    elif index+1==len(sent):
      tfeat.append('__EOS__')
    features.append(tfeat)
  return features

if __name__=='__main__':
  lang=sys.argv[1]
  trie=pickle.load(open(lang+'.marisa'))
  trainer=pycrfsuite.Trainer(algorithm='pa',verbose=True)
  trainer.set_params({'max_iterations':10})
  for sent in conll_iter(open('training_data/'+lang+'.conll')):
    #print sent
    tokens=[e[1] for e in sent]
    labels=[e[4] for e in sent]
    #print labels
    feats=extract_features_msd(tokens,trie)
    trainer.append(feats,labels)
    #break
  trainer.train(lang+'.msd.model')
