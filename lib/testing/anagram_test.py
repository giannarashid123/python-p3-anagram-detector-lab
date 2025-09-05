from lib.anagram import Anagram

def test_single_anagram_match():
    listen = Anagram("listen")
    assert listen.match(['enlists', 'google', 'inlets', 'banana']) == ['inlets']

def test_no_anagrams():
    hello = Anagram("hello")
    assert hello.match(['world', 'python', 'java']) == []

def test_case_insensitive():
    master = Anagram("Master")
    result = master.match(['stream', 'maters', 'Steamr'])
    assert sorted(result) == sorted(['stream', 'maters', 'Steamr'])

def test_exact_word_not_included():
    dog = Anagram("dog")
    assert dog.match(['dog', 'god', 'gdo']) == ['god', 'gdo']
