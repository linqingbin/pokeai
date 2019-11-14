import math
import csv
import numpy as np
import logging
from settings import TYPE_MAP_FILE_PATH, MODIFIER_RATIO_CHECK, STRATEGY_WEIGHT_MAP, SYMBOL_MODIFIER_MAP


class PokeDoctor(object):

    def __init__(self, strategy="balance"):
        '''
        strategy: String, balance, attack or defense
        '''
        self.typeMapMat, self.types = getTypeMapMat()
        self.strategy = strategy

    def getReport(self, existsTypes, topN=3):
        '''
        获得针对当前组合的分析报告
        return dict
        '''
        report = self._analyse(existsTypes)
        nextTypeRank = self._recommendNextType(existsTypes)
        report['next'] = [x[0] for x in nextTypeRank][:topN]
        report['nextTypeRank'] = nextTypeRank
        return report

    def getRecommend(self, existsTypes, topN=3):
        '''
        仅仅获得推荐内容
        '''
        report = {}
        nextTypeRank = self._recommendNextType(existsTypes)
        report['next'] = [x[0] for x in nextTypeRank][:topN]
        report['nextTypeRank'] = nextTypeRank
        return report

    def _recommendNextType(self, existsTypes):
        '''
        获得针对当前组合的下一个属性的推荐列表
        return list
        '''
        scoreDict = {}
        for optionType in self.types:
            if optionType in existsTypes:
                continue
            else:
                newParty = existsTypes + [optionType]
                # oldReport = self._analyse(existsTypes)
                newReport = self._analyse(newParty)
                # oldScore = oldReport['score']
                newScore = newReport['score']

                scoreDict[optionType] = newScore
        typeRank = sorted(scoreDict.items(),
                          key=lambda x: x[1], reverse=True)
        return typeRank

    def _analyse(self, existsTypes):
        '''
        分析当前组合对每个属性的优劣势及其综合分
        return dict
        '''
        existsTypeIndexes = [self.types.index(
            existsType) for existsType in existsTypes]
        # defenseMat = self.typeMapMat[:, existsTypeIndexes]
        # attackMat = self.typeMapMat[existsTypeIndexes, :]
        details = []
        weights = STRATEGY_WEIGHT_MAP[self.strategy]
        for i, optionType in enumerate(self.types):
            # print(optionType)
            # 将当前的属性组合对每个对抗属性进行防御和攻击的综合分的评估
            # 注意弱点不仅是防御，优势不仅是攻击
            defenseModifiers = self.typeMapMat[i, existsTypeIndexes].tolist()
            attackModifiers = self.typeMapMat[existsTypeIndexes, i].tolist()
            defenseScore = scoreModifiers(defenseModifiers, flag="defense")
            attackScore = scoreModifiers(attackModifiers, flag="attack")
            score = ratioMean(np.array(
                [defenseScore ** weights["defense"], attackScore ** weights["attack"]]))
            details.append([defenseScore, attackScore, score])
        sortedTypeDetails = sorted(zip(self.types, details),
                                   key=lambda x: (x[1][2], x[1][1]), reverse=True)
        finalScore = ratioMean(np.array(details)[:, 2])
        report = {
            "exists": existsTypes,
            "weakness": list(reversed([x[0] for x in sortedTypeDetails[-3:]])),
            "goodness": [x[0] for x in sortedTypeDetails[:3]],
            "details": sortedTypeDetails,
            "score": finalScore,
            "options": self.types,
            "method": self.strategy
        }
        return report


def ratioMean(ratiosArr):
    return ratiosArr.prod() ** (1/len(ratiosArr))


def scoreModifiers(modifiers: list, flag: str):
    '''
    分析组合对某个属性的修正系数的评分。
    基本规则是：
    * modifiers的长度等于组合的长度
    * 先将modifier转化为ratio，ratio的范围0.25到4
    * 如果存在多个显著，数量越多，得分增幅越低。

    例如flag为attack，我方火、水、草对于刚属性的ratio是[0.5,0.5,0.5]，则相比与火、水的[0.5,0.5]，得分应该下降，但是降幅应该减缓
    例如flag为attack，我方冰、火、岩石对于飞行属性的ratio是[2,2,2]，则相比与冰、火的[2,2]，得分应该上升，但是升幅应该减缓

    params:
        flag: String, attack or defense

    return:
        score: float
    '''
    ratios = [MODIFIER_RATIO_CHECK[i][flag]
              for i in modifiers]    # 对每个属性的优劣势表
    ratiosArr = np.array(ratios)
    score = np.round(ratiosArr.prod() ** (1/len(ratiosArr)), 2)
    return score


def getTypeMapMat():
    '''获得属性映射表'''
    with open(TYPE_MAP_FILE_PATH, "r", encoding="utf-8") as f:
        channel = csv.reader(f)
        data = [x for x in channel]
    arr = np.array(data)
    types = [x.replace("\xa0", "") for x in arr[0, :][1:]]
    relations = arr[1:, 1:]
    typeMapMat = np.array([[symbol2modifier(x) for x in row]
                           for row in relations])
    return typeMapMat, types


def symbol2modifier(symbol):
    '''
    关系符号转化为数字。注意这里的×不是x，1⁄2也不是1/2。
    '''
    value = symbol.replace("×", "")
    modifier = SYMBOL_MODIFIER_MAP.get(value, "1")
    return modifier
