import sys
import argparse
import json
import random
import polars as pl
import pandas as pd
from common import SENTENCES_FILE, stdout_redirected

def load_data():
    with open(SENTENCES_FILE, 'r') as file:
        data = json.JSONDecoder().decode(file.read())
    texts, index = data['texts'], data['index']
    sentences = []
    for text in texts:
        sentences.extend(text['sentences'])
    return texts, sentences, index

def show_grammatical_homonymy(texts, index, max_examples=5):
    example_count = 0
    keys = list(index.keys())
    random.shuffle(keys)
    for word in keys:
        docs = index[word]
        form_pos = {}
        for text_id, sent_id in docs:
            sentence = texts[text_id]['sentences'][sent_id]
            for token in sentence['tokens']:
                if token['lemma'] == word:
                    text = token['text'].lower()
                    if text not in form_pos:
                        form_pos[text] = {}
                    form_pos[text][token['upos']] = sentence['original']
        for form, pos in form_pos.items():
            if len(pos) > 1:
                print('-'*20)
                print(f'Примеры для слова "{form}":')
                for upos, sent in pos.items():
                    print(f'{upos}:\t{sent}')
                example_count += 1
                if example_count == max_examples:
                    return
                break

def show_lexical_homonymy(texts, index, words, max_sent=20):
    for word in words:
        print('-'*20)
        print(f'Примеры для слова {word}')
        for text_id, sent_id in index[word][:max_sent]:
            print('-'*10)
            print(texts[text_id]['sentences'][sent_id]['original'])

def _ljust(s):
    s = s.astype(str).str.strip()
    return s.str.ljust(s.str.len().max())

def morphological_analysis(sentence):
    pd.options.display.max_colwidth = 100
    df = pl.DataFrame(sentence['tokens'])
    df = df.select([
        pl.col('text').alias('Слово'),
        pl.col('upos').alias('Часть речи'),
        pl.col('feats').alias('Морфологический разбор')
    ])
    return df.to_pandas().apply(_ljust).to_string(index=False)

def show_morphological_analysis(sentences, count=1, min_len=10):
    random_sentences = random.choices(sentences, k=count+10)
    processed = 0
    for sentence in random_sentences:
        if len(sentence['tokens']) < min_len:
            continue
        print('-'*20)
        print(sentence['original'])
        print()
        print(morphological_analysis(sentence))
        processed += 1
        if processed == count:
            return

def show_non_tree(sentences):
    for sentence in sentences:
        if len(sentence['tokens']) < 5:
            continue
        is_verb = False
        for token in sentence['tokens']:
            if token['upos'] == 'VERB' or token['upos'] == 'ADV':
                is_verb = True
                break
        if not is_verb:
            print(sentence['original'])

def show_graph(id, graph, tokens, deep=0):
    print('|\t'*deep, tokens[id]['text'], sep='')
    for child in graph[id]:
        show_graph(child, graph, tokens, deep + 1)

def show_dependencies(sentences, count=1, min_len=10):
    random_sentences = random.choices(sentences, k=count+10)
    processed = 0
    for sentence in random_sentences:
        if len(sentence['tokens']) < min_len:
            continue
        print('-'*20)
        print(sentence['original'])
        print()
        graph = [[] for _ in range(len(sentence['tokens']))]
        for token in sentence['tokens']:
            cur_id = token['id'] - 1
            head = token['head'] - 1
            if head < 0:
                root = cur_id
            else:
                graph[head].append(cur_id)
        show_graph(root, graph, sentence['tokens'])
        processed += 1
        if processed == count:
            return

def make_morf_analysis(texts, index, sentences, command):
    print(command)
    command = command.strip().split('\t', 1)[-1]
    for sentence in sentences:
        if command == sentence['original']:
            print(morphological_analysis(sentence))
            return 1
    return 0

if __name__ == '__main__':
    texts, sentences, index = load_data()
    file_name = sys.argv[1]
    line_count = -1
    if len(sys.argv) > 2:
        line_count = int(sys.argv[2])
    processed = 0
    with open(file_name, 'r') as file:
        for line in file:
            processed += make_morf_analysis(texts, index, sentences, line)
            if processed == line_count:
                break
