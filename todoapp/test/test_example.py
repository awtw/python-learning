def test_equal_or_not_equal():
    assert 1 == 1
    assert 1 != 2
    assert 1 != "2"
    assert 1 == True
    assert 1 != False
    assert 1 != [1, 2, 3]
    assert 1 != {1, 2, 3}
    assert 1 != (1, 2, 3)

