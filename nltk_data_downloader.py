import os


def download():
    import nltk
    file_path = os.path.dirname(__file__)
    nltk.data.path.append(
        os.path.join(file_path, './nltk_data')
    )
    if not os.path.exists('./nltk_data'):
        nltk.download(
            ['maxent_treebank_pos_tagger', 'punkt'],
            download_dir='./nltk_data'
        )
