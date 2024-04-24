from typing import List

from app.database.repositories.repo import repo

from sklearn.feature_extraction.text import TfidfVectorizer


def get_data() -> list[dict]:
    files = repo.get_all_files()
    documents = [file.content.decode("utf-8") for file in files]
    words = get_words(documents)
    all_words = sum(words, [])
    data = []
    for word in get_unique(words):
        row = {}
        row["word"] = word
        row["tf"] = get_tf(word, all_words)
        row["idf"] = get_idf(word, documents)
        data.append(row)
    return data


def get_unique(lists: list[ list[str]]) -> list[str]:
    all_lists = []
    for list_ in lists:
        all_lists += list_
    return list(set(all_lists))


def get_tf(refer_word: str, words: List[str]) -> int:
    return words.count(refer_word)


def get_idf(refer_word: str, documents: list[list [str]]) -> float:
    # documents = list(documents)
    # total_documents = len(documents)
    # documents_containing_word = sum(1 for document in documents if refer_word in document)
    # idf = math.log(total_documents / (1 + documents_containing_word))
    # return idf
    corpus = documents.copy()
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(corpus)
    feature_names = vectorizer.get_feature_names_out()
    try:
        word_index = list(feature_names).index(refer_word)
    except ValueError:
        return 0.0

    return X[0, word_index]


def get_words(documents: list[str]) -> list[ list[str] ]:
    serialized_docs = [serialize_doc(document) for document in documents]  # TODO: изменить нейминг
    lists_of_words = [doc_to_list(doc) for doc in serialized_docs]
    return lists_of_words


def doc_to_list(lines: str) -> list[str]:
    return [word.strip().lower() for word in lines.split(" ") if word != ""]


def serialize_doc(text: str) -> str:
    filter_characters = text
    extra_characters = "\n\t.,,;:!?/+=-(){}[]*&^%$#@№\"''-=~|\\"
    for character in text:
        if character in extra_characters:
            filter_characters = filter_characters.replace(character, " ")
    return filter_characters

# repo.delete_all_file()
# print(repo.get_all_files())