import numpy as np
import pandas as pd
import json

df = pd.read_csv('data/food_nutritions.csv')
col_list = ['NameEng', 'NameVn', 'Nutritions']
nparr = np.array(df[col_list])
for x in nparr:
    try:
        x[2] = json.loads(x[2].replace('"', '"'))
    except:
        print(x[0], x[2])

def get_nparr():
    return nparr
        
def entity_to_nutri(entity):
    entity_to_food = {'advantage': 'none', 'apple': 'apple', 'banana': 'Banana','beef': 'beef','broccoli': 'broccoli','buffalo': 'buffalo','cabbage': 'cabbage','Carb': 'none','chicken': 'chicken','crab': 'crab','disadvantage': 'none','duck': 'duck','Energy': 'none','fat': 'none','general_atrributes_food': 'none','gen_fish': 'fish','guava': 'guava','lamb': 'lamb','orange': 'Orange','Protein': 'none', 'pumpkin': 'pumpkin','shrimp': 'shrimp','squid': 'squid','Water': 'Water','water_spiniach': 'water spinach' }
    
    food_name = entity_to_food[entity]

    nutri_order = [['Energy', 0], ['Total lipid (fat)', 1], ['Protein', 2], ['Sodium, Na', 3], ['Calcium, Ca', 4], ['Carbohydrate, by difference', 5], ['Iron, Fe', 6], ['Water', 7], ['Phosphorus, P', 8], ['Potassium, K', 9], ['Niacin', 10], ['Magnesium, Mg', 11], ['Riboflavin', 12], ['Thiamin', 13], ['Zinc, Zn', 14], ['Vitamin B-6', 15], ['Fatty acids, total saturated', 16], ['Vitamin C, total ascorbic acid', 17], ['Folate, DFE', 18], ['Vitamin A, IU', 19], ['Fatty acids, total polyunsaturated', 20], ['Fatty acids, total monounsaturated', 21], ['Fiber, total dietary', 22], ['Vitamin A, RAE', 23], ['Sugars, total', 24], ['Vitamin E (alpha-tocopherol)', 25], ['Vitamin K (phylloquinone)', 26], ['Cholesterol', 27], ['Vitamin B-12', 28], ['Vitamin D', 29], ['Vitamin D (D2 + D3)', 30], ['Fatty acids, total trans', 31]]
    nutri_order = {tmp1:tmp2 for tmp1, tmp2 in nutri_order}
    for tmp in nparr:
        if tmp[0] == food_name:
            nutri_list = []
            for k,v in tmp[2].items():
                    tmp = v.split(' ')
                    if float(tmp[0]) > 0 and len(tmp) == 2:
                        nutri_list.append([k,v])
            nutri_list = sorted(nutri_list, key=lambda x: nutri_order[x[0]])
            nutri_list = '\n'.join([f'100g {entity} contains: '] + [tmp1 + ', ' + tmp2 for tmp1, tmp2 in nutri_list])
            return nutri_list
    return 'Food doesnt not exist in database'