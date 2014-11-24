import os


def download():
    import nltk
    nltk.data.path.append(os.path.join('./nltk_data'))
    if not os.path.exists('./nltk_data'):
        nltk.download(
            ['maxent_treebank_pos_tagger', 'punkt'],
            download_dir='./nltk_data'
        )
