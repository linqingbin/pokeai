
import pokeai


def test_getTypeMapMat():
    mat, types = pokeai.getTypeMapMat()
    assert isinstance(mat[0, 0], str)
    assert isinstance(types, list)


def test_symbol2modifier():
    cases = [
        ('1×', "1"),
        ('2×', "2"),
        ('1⁄2×', "1/2"),
        ('0×', "0")
    ]
    for case in cases:
        para, expected = case
        assert pokeai.symbol2modifier(para) == expected


def test_scoreModifiers():
    cases = [
        (["1", "2", "1/2"], "attack",  -1),
        (["1", "1", "2"], "defense", -1),
        (["1", "2", "2"], "attack", 0),
        (["1", "1/2", "1/2"], "defense", 0),
    ]
    for case in cases:
        arr, flag, minValue = case
        score = pokeai.scoreModifiers(arr, flag)
        assert score > minValue


def test_PokeDoctor_report():
    cases = [
        (["Fire", "Grass", "Water"], ["Dragon"], ["Ground"]),
    ]
    doctor = pokeai.PokeDoctor()
    for case in cases:
        existsTypes, weakness, goodness = case
        report = doctor.getReport(existsTypes)
        print(report)
        for x in weakness:
            assert x in report['weakness']
        for y in goodness:
            assert y in report['goodness']
