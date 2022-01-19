"""
utils

main functions:
prefilter_items
postfilter_items
get_recommendations
get_similar_items_recommendation
get_similar_users_recommendation
"""

def prefilter_items(data, item_features, take_n_popular):
    # Уберем самые популярные товары (их и так купят)
    popularity = data.groupby('item_id')['user_id'].nunique().reset_index()
    popularity.rename(columns={'user_id': 'unique_users_bought'}, inplace=True)
    popularity['unique_users_bought'] = popularity['unique_users_bought'] / data['user_id'].nunique()
    
    top_popular = popularity[popularity['unique_users_bought'] > 0.5].item_id.tolist()
    data = data[~data['item_id'].isin(top_popular)]
    
    # Уберем самые НЕ популярные товары (их и так НЕ купят)
    top_notpopular = popularity[popularity['unique_users_bought'] < 0.01].item_id.tolist()
    data = data[~data['item_id'].isin(top_notpopular)]
    
    #ограничимся списком товаров до take_n_popular
    popularity = data.groupby('item_id')['user_id'].nunique().reset_index()    
    popularity.rename(columns={'user_id': 'unique_users_bought'}, inplace=True)
    if popularity.shape[0] > take_n_popular:
        popularity.sort_values('unique_users_bought', ascending=False, inplace=True)
        n_popular = popularity[:take_n_popular].item_id.tolist()
    data = data[~data['item_id'].isin(n_popular)]
    # Уберем товары, которые не продавались за последние 6 месяцев(26 недель)
    # не понятно по какой колонке смотреть ближайшую дату продажи: day, week_no???
    old_goods = data.groupby('item_id')['week_no'].min().reset_index()
    top_old = old_goods[old_goods['week_no'] > 26].item_id.tolist()
    data = data[~data['item_id'].isin(top_old)]
    
    # Уберем не интересные для рекоммендаций категории (department)
    
    # Уберем слишком дешевые товары (на них не заработаем). 1 покупка из рассылок стоит 60 руб.
    # не понятно откуда брать стоимость товара ??? sales_value??? вроде объем продаж
    #goods_median_price = data.groupby('item_id')['sales_value'].median().reset_index()
    
    # Уберем слишком дорогие товары
    
    # ...
    return data
    
def postfilter_items(user_id, recommednations):
    pass

def get_recommendations(user, model, sparse_user_item, N=5):
    """Рекомендуем топ-N товаров"""
    
    res = [id_to_itemid[rec[0]] for rec in 
                    model.recommend(userid=userid_to_id[user], 
                                    user_items=sparse_user_item,   # на вход user-item matrix
                                    N=N, 
                                    filter_already_liked_items=False, 
                                    filter_items=[itemid_to_id[999999]],  # !!! 
                                    recalculate_user=True)]
    return res

def get_similar_items_recommendation(user, model, N=5):
    """Рекомендуем товары, похожие на топ-N купленных юзером товаров"""
    
    # your_code
    
    return res

def get_similar_users_recommendation(user, model, N=5):
    """Рекомендуем топ-N товаров, среди купленных похожими юзерами"""
    
    # your_code
    
    return res

def weighted_random_recommendation(items_weights, n=5):
    """Случайные рекоммендации
    
    Input
    -----
    items_weights: pd.DataFrame
        Датафрейм со столбцами item_id, weight. Сумма weight по всем товарам = 1
    """
    
    # Подсказка: необходимо модифицировать функцию random_recommendation()
    # your_code
    recs = np.random.choice(items_weights['item_id'], size=n, replace=False, p=items_weights['weight'])
    return recs.tolist()
