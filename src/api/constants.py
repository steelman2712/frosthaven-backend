
def get_level(exp):
    levels = [1]
    for exp_needed in EXP_LEVEL.keys():
        if exp >= exp_needed: 
            levels.append(EXP_LEVEL[exp_needed])
    return max(levels)
    

EXP_LEVEL = {
    0 : 1,
    45 : 2,
    95 : 3,
    150 : 4,
    210 : 5,
    275 : 6,
    345 : 7,
    420 : 8,
    500 : 9
}
