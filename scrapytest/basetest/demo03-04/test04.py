# -*- coding: utf-8 -*-
__author__ = 'zciel'

import pandas as pd

test_dict = {'id':[1,2,3,4,5,6],'name':['Alice','Bob','Cindy','Eric','Helen','Grace '],'math':[90,89,99,78,97,93],'english':[89,94,80,94,94,90]}
#[1].直接写入参数test_dict
# test_dict_df = pd.DataFrame(test_dict)
#[2].字典型赋值
# test_dict_df = pd.DataFrame(data=test_dict)


test_dict_df = pd.DataFrame.from_dict(test_dict)

test_dict_df