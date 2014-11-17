import nltk
import os
nltk.data.path.append(
    os.path.join(os.path.dirname(__file__), '../../nltk_data')
)


# Inspired by Finn Nielsens code from Data Mining using Python 02819 at DTU.
class TextChunkifier(object):
    def text_chunks(self, text):
        return self._extract_chunks(
            self._grammar_parser().parse(
                nltk.pos_tag(
                    nltk.word_tokenize(text)
                )
            )
        )

    def _extract_chunks(self, tree, tree_filter='NP'):
        chunks = []
        if hasattr(tree, 'label'):
            if tree.label() == tree_filter:
                leafWords = map(self._extract_word_from_leaf, tree.leaves())
                chunks = [" ".join(leafWords)]
            else:
                for child in tree:
                    cs = self._extract_chunks(child, tree_filter=tree_filter)
                    if cs != []:
                        chunks.append(cs[0])
        return chunks

    def _extract_word_from_leaf(self, leaf):
        return leaf[0].lower()

    def _grammar_parser(self):
        return nltk.RegexpParser("NP: { <JJ>*<NN.?>+ }")
