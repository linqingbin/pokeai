import csv
import numpy as np

TYPE_AGANIST_FILE_PATH = "typeAganist.csv"

# 新属性被其他属性攻击的显著性得分，越显著得分越低
DEFENCE_ADD = {
    "2": 0,
    "1/2": 2,
    "0": 4,
    "1": 1
}

# 既有属性被其他属性攻击的显著性系数加成，越显著系数越高，默认为1
DEFENCE_COEF = {
    "2": 2,
    "1/2": 0.5,
    "0": 0,
    "1": 1
}

# 新属性攻击其他属性的显著性得分，越显著得分越高
ATTACK_ADD = {
    "2": 2,
    "1/2": 0.5,
    "0": 0,
    "1": 1
}

# 既有属性攻击其他属性的显著性系数加成，越显著系数越低，默认为1
ATTACK_COEF = {
    "2": 0.5,
    "1/2": 2,
    "0": 4,
    "1": 1
}

GOOD_WEAK_CHECK = {
    "2": {
        "attack": 2,
        "defense": 0.5
    },
    "1/2": {
        "attack": 0.5,
        "defense": 2
    },
    "1": {
        "attack": 1,
        "defense": 1
    },
    "0": {
        "attack": 0,
        "defense": 4
    },
}


def getTypeAganistMatrix():
    with open(TYPE_AGANIST_FILE_PATH, "r", encoding="utf-8") as f:
        channel = csv.reader(f)
        data = [x for x in channel]
    arr = np.array(data)
    types = [x.replace("\xa0", "") for x in arr[0, :][1:]]
    relations = arr[1:, 1:]
    numberMat = np.array([[symbol2number(x) for x in row]
                          for row in relations])
    return numberMat, types


class PokeDoctor(object):

    def __init__(self):
        self.typeAganistMat, self.types = getTypeAganistMatrix()

    def selectBestNextType(self, existsTypes, mehtod="balance"):
        scoreDict = {}
        for optionType in self.types:
            if optionType in existsTypes:
                continue
            else:
                socre = self._scoreType(existsTypes, optionType)
                scoreDict[optionType] = socre
        sortedIems = sorted(scoreDict.items(),
                            key=lambda x: x[1], reverse=True)
        bestNextType, bestScore = sortedIems[0]
        return bestNextType, bestScore, sortedIems

    def selectBestNextType2(self, existsTypes, mehtod="balance"):
        scoreDict = {}
        for optionType in self.types:
            if optionType in existsTypes:
                continue
            else:
                party = existsTypes + [optionType]
                report = self.analyse(party)
                score = report['totalScore']
                scoreDict[optionType] = score
        sortedIems = sorted(scoreDict.items(),
                            key=lambda x: x[1], reverse=True)
        bestNextType, bestScore = sortedIems[0]
        return bestNextType, bestScore, sortedIems

    def getReport(self, existsTypes):
        bestNextType, bestScore, sortedIems = self.selectBestNextType2(
            existsTypes)
        report = self.analyse(existsTypes)
        report['bestNextTypes'] = [x[0] for x in sortedIems][:3]
        report['existsTypes'] = existsTypes
        report['optionTypes'] = self.types        
        return report

    def scoreParty(self, existsTypes):
        '''
        '''
        pass

    def _scoreType(self, existsTypes, newType, method="balance"):
        '''
        scoreMethod:balance,attack,defence
        '''
        newTypeIndex = self.types.index(newType)
        # valuate defend
        defenseScore = 0
        attackScore = 0
        for part in ['defense', 'attack']:
            if part == 'defense':
                aganistRow = self.typeAganistMat[:, newTypeIndex]
                addDict = DEFENCE_ADD
                coefDict = DEFENCE_COEF
            else:
                aganistRow = self.typeAganistMat[newTypeIndex, :]
                addDict = ATTACK_ADD
                coefDict = ATTACK_COEF
            for i, value in enumerate(aganistRow):
                add = addDict[value]
                coef = 1
                for existsType in existsTypes:
                    existsTypeIndex = self.types.index(existsType)
                    if part == "defense":
                        existsValue = self.typeAganistMat[i, existsTypeIndex]
                    else:
                        existsValue = self.typeAganistMat[existsTypeIndex, i]
                    coef *= coefDict[existsValue]
                record = add * coef
                if part == "defense":
                    defenseScore += record
                else:
                    attackScore += record
        if method == "balance":
            weight = (0.5, 0.5)
        elif method == "defense":
            weight = (0.75, 0.25)
        elif method == "attack":
            weight = (0.25, 0.75)
        defenseScoreWeight, attackScoreWeight = weight
        finalScore = defenseScoreWeight*defenseScore + attackScoreWeight*attackScore
        return finalScore

    def analyse(self, existsTypes):
        '''
        分析某个组合的优劣势
        '''
        existsTypeIndexes = [self.types.index(
            existsType) for existsType in existsTypes]
        defenseMat = self.typeAganistMat[:, existsTypeIndexes]
        attackMat = self.typeAganistMat[existsTypeIndexes, :]
        scores = []
        scoreMat = []
        for i in range(len(self.types)):
            defenseScore, attackScore = scoreParty(
                defenseMat[i, :], attackMat[:, i])
            scoreMat.append([defenseScore, attackScore])
            score = np.mean([defenseScore, attackScore])
            scores.append(score)
        scoreMat = np.array(scoreMat)
        sortedTypes = sorted(zip(self.types, scores),
                             key=lambda x: x[1], reverse=True)
        report = {
            "weakness": list(reversed([x[0] for x in sortedTypes[-3:]])),
            "goodness": [x[0] for x in sortedTypes[:3]],
            "scoreMat": scoreMat,
            "totalScore": np.round(scoreMat.mean(), 2)
        }
        return report


def scoreParty(defenseArr, attackArr):
    scores = []
    for flag, arr in [('defense', defenseArr), ('attack', attackArr)]:
        goodWeak = [GOOD_WEAK_CHECK[i][flag] for i in arr]
        score = scoreGoodWeak(goodWeak)
        scores.append(np.round(score, 2))
    defenseScore, attackScore = scores
    return (defenseScore, attackScore)


def scoreGoodWeak(goodWeak):
    molecule = 0
    denominator = 0
    for x in goodWeak:
        if x >= 2:
            molecule += x * 2
            denominator += 2
        else:
            molecule += x
            denominator += 1
    if denominator > 0:
        return molecule/denominator
    else:
        return 0


def numebr2coef(number):
    pass


def symbol2number(symbol):
    '''
    关系符号转化为数字。注意这里的×不是x，1⁄2也不是1/2。
    '''
    value = symbol.replace("×", "")
    if value == "0":
        number = "0"
    elif value == "1⁄2":
        number = "1/2"
    elif value == "2":
        number = "2"
    else:
        number = "1"
    return number
