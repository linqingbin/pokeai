TYPE_MAP_FILE_PATH = "data/typeMapEn.csv"

# 效果强弱量化表：GOOD_WEAK_CHECK
# 2：代表效果拔群
# 1/2：代表效果不怎么样
# 1：代表效果普通
# 0：代表无效
# 指定Key下的attack代表当攻属攻击防属时的效果情况，然后基于评分，评分越高，代表越优秀。
# 因为之后会取对数进行比较，所以最小值为0.25，最大值为4。log(0.25) = -log(4)

SYMBOL_MODIFIER_MAP = {
    "0": "0",
    "1⁄2": "1/2",
    "2": "2"
}

MODIFIER_RATIO_CHECK = {
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
        "attack": 0.25,
        "defense": 4
    },
}

STRATEGY_WEIGHT_MAP = {
    "balance": {
        "defense": 1,
        "attack": 1,
    },
    "attack": {
        "defense": 0.5,
        "attack": 2,
    },
    "defense": {
        "defense": 2,
        "attack": 0.5,
    },

}


