
import pokeai


def test_getTypeAganistMatrix():
    mat, types = pokeai.getTypeAganistMatrix()
    assert isinstance(mat[0, 0], str)
    assert isinstance(types, list)


def test_symbol2number():
    cases = [
        ('1×', "1"),
        ('2×', "2"),
        ('1⁄2×', "1/2"),
        ('0×', "0")
    ]
    for case in cases:
        para, expected = case
        assert pokeai.symbol2number(para) == expected


def test_PokeDoctor_score():
    cases = [
        (["飞行", "草"], "地面", "虫"),
        (["水", "岩石"], "火", "超能力")
    ]
    doctor = pokeai.PokeDoctor()
    for case in cases:
        existsTypes, betterType, worseType = case
        leftScore = doctor._scoreType(existsTypes, betterType)
        rightScore = doctor._scoreType(existsTypes, worseType)
        print(case, leftScore, rightScore)
        assert leftScore > rightScore
        reprot = doctor.getReport(existsTypes)
        print(reprot)


def test_PokeDoctor_analyse():
    cases = [
        (["飞行", "草"], ["冰"], ["格斗", "地面"]),
        (["水", "岩石"], ["草"], ["火"]),
        (["飞行", "草", "毒", "地面"], ["冰"], ["草"])
    ]
    doctor = pokeai.PokeDoctor()
    for case in cases:
        existsTypes, weakness, goodness = case
        report = doctor.analyse(existsTypes)
        for x in weakness:
            assert x in report['weakness']
        for y in goodness:
            assert y in report['goodness']


def test_scoreParty():
    cases = [
        (["1", "2", "1/2"], ["1", "1", "2"], 1),
        (["1", "2", "2"], ["1", "1", "1"], 0),
    ]
    for case in cases:
        defenseArr, attackArr, minValue = case
        defenseScore, attackScore = pokeai.scoreParty(defenseArr, attackArr)
        score = (defenseScore+attackScore)/2
        assert score > minValue
