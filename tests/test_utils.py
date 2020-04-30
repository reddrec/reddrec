from reddrec.utils import lookup_table

def test_lookup_table():
    xs = ['e', 'v', 'a', 'n']
    index = lookup_table(xs)
    expected = {
        'e': 0,
        'v': 1,
        'a': 2,
        'n': 3
    }

    assert expected == index
