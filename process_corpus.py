import stanza
stanza.download('ru')
import json
import time
import argparse
import sys
from common import TEXTS_FILE, SENTENCES_FILE

def build_inverted_index(texts):
    index = {}
    for text_id, text in enumerate(texts):
        for sent_id, sentence in enumerate(text['sentences']):
            for word in sentence['tokens']:
                v = word.lemma
                if v not in index:
                    index[v] = []
                index[v].append((text_id, sent_id))
    return index


def process(texts):
    pipeline = stanza.Pipeline('ru', processors='tokenize,pos,lemma,depparse')
    text_count = len(texts)
    for text_id, text_info in enumerate(texts):
        text = pipeline(text_info['content'])
        sentences = []
        for sentence in text.sentences:
            tokens = sentence.words
            original = ' '.join(list(map(lambda x: x.text, tokens)))
            sentence = {'tokens': tokens, 'original': original}
            sentences.append(sentence)
        text_info['sentences'] = sentences
        del text_info['content']
        print(f'Processing: {round((text_id + 1) / text_count * 100, 2)}% completed')
    inverted_index = build_inverted_index(texts)
    return texts, inverted_index


if __name__ == '__main__':
    with open(TEXTS_FILE, 'r') as file:
        texts = json.JSONDecoder().decode(file.read())
    result = {}
    result['texts'], result['index'] = process(texts)

    with open(SENTENCES_FILE, 'w') as file:
        json.dump(result, file)