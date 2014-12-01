"""Downloads nltk data relevant for the cv kickstarter project.

If any new module needs data from nltk, it should be added here.
"""
import os


def download():
    """Download relevant nltk data for cv kickstarter.

    If there already exists a nltk_data folder in the root, it is not
    downloaded.

    If nltk data is added the nltk_data folder need to be removed for
    downloading the new data.
    """
    import nltk
    nltk.data.path.append(os.path.join('./nltk_data'))
    if not os.path.exists('./nltk_data'):
        nltk.download(
            ['maxent_treebank_pos_tagger', 'punkt'],
            download_dir='./nltk_data'
        )
