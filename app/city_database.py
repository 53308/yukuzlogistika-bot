# -*- coding: utf-8 -*-
"""
Comprehensive City Database for Logistics Bot
Includes ALL possible variants: Latin, Cyrillic, grammatical forms, special characters
"""

# Massive city database with all possible variants
CITY_VARIANTS = {
    # === TASHKENT / ТАШКЕНТ ===
    'toshkent': ['ташкент', 'toshkent', 'tashkent', 'tosh-kent', 'tash-kent', 'towkent', 
                'toshkent shahri', 'tashkent city', 'toshkentga', 'tashkentga', 'toshkentdan', 
                'tashkentdan', 'toshkentda', 'toshkentdagi', 'toshkenga', 'toshkentga',
                'olmosga', 'olmosxoja', 'olmos', 'olmoscha', 'тошкент', 'ташкент', 
                'тош-кент', 'таш-кент', 'товкент', 'тошкент шаҳри', 'город ташкент',
                'ташкента', 'ташкенте', 'ташкенту', 'ташкентский', 'ташкент-сити', 'toshkentskiy'],
    
    'tashkent': ['ташкент', 'toshkent', 'tashkent', 'tosh-kent', 'tash-kent', 'towkent', 
                'toshkent shahri', 'tashkent city', 'toshkentga', 'tashkentga', 'toshkentdan', 
                'tashkentdan', 'toshkentda', 'toshkentdagi', 'toshkenga', 'toshkentga',
                'olmosga', 'olmosxoja', 'olmos', 'olmoscha', 'тошкент', 'ташкент', 
                'тош-кент', 'таш-кент', 'товкент', 'тошкент шаҳри', 'город ташкент',
                'ташкента', 'ташкенте', 'ташкенту', 'ташкентский', 'ташкент-сити', 'toshkentskiy'],
    
    'ташкент': ['ташкент', 'toshkent', 'tashkent', 'tosh-kent', 'tash-kent', 'towkent', 
               'toshkent shahri', 'tashkent city', 'toshkentga', 'tashkentga', 'toshkentdan', 
               'tashkentdan', 'toshkentda', 'toshkentdagi', 'toshkenga', 'toshkentga',
               'olmosga', 'olmosxoja', 'olmos', 'olmoscha', 'тошкент', 'ташкент', 
               'тош-кент', 'таш-кент', 'товкент', 'тошкент шаҳри', 'город ташкент',
               'ташкента', 'ташкенте', 'ташкенту', 'ташкентский', 'ташкент-сити', 'toshkentskiy'],
               
    # Tashkent Oblast
    'toshkent viloyati': ['тошкент вилояти', 'ташкентская область', 'toshkent viloyati', 'tashkent oblast', 
                         'toshkent region', 'toshkent viloyatiga', 'toshkent viloyatidan', 'toshkent viloyatda'],
    
    # === JIZZAKH / ЖИЗЗАХ ===
    'jizzax': ['жиззах', 'джизак', 'jizzax', 'jizzakh', 'jizzax shaxri', 'jizzax city',
               'jizzaq', 'jizzaq zomin', 'jizzaq zomindan', 'jizzaxda', 'jizzaxdan', 
               'jizzaxga', 'jizzaxlik', 'гагарин', 'gagarin', 'гагариндан', 'gagarindan'],
               
    'жиззах': ['жиззах', 'джизак', 'jizzax', 'jizzakh', 'jizzax shaxri', 'jizzax city',
               'jizzaq', 'jizzaq zomin', 'jizzaq zomindan', 'jizzaxda', 'jizzaxdan', 
               'jizzaxga', 'jizzaxlik', 'гагарин', 'gagarin', 'гагариндан', 'gagarindan'],
               
    'джизак': ['жиззах', 'джизак', 'jizzax', 'jizzakh', 'jizzax shaxri', 'jizzax city',
               'jizzaq', 'jizzaq zomin', 'jizzaq zomindan', 'jizzaxda', 'jizzaxdan', 
               'jizzaxga', 'jizzaxlik', 'гагарин', 'gagarin', 'гагариндан', 'gagarindan'],
    
    # === SAMARKAND / САМАРКАНД ===
    'samarqand': ['самарканд', 'samarqand', 'samarkand', 'samarqandga', 'samarqanddan', 
                  'samarqandda', 'samarqand shahri', 'самарканда', 'самарканде', 'самарканду'],
    'samarkand': ['самарканд', 'samarqand', 'samarkand', 'samarqandga', 'samarqanddan', 
                  'samarqandda', 'samarqand shahri', 'самарканда', 'самарканде', 'самарканду'],
    'самарканд': ['самарканд', 'samarqand', 'samarkand', 'samarqandga', 'samarqanddan', 
                  'samarqandda', 'samarqand shahri', 'самарканда', 'самарканде', 'самарканду'],
    
    # === NAMANGAN / НАМАНГАН ===
    'namangan': ['наманган', 'namangan', 'namanganga', 'namangandan', 'namanganda', 
                'namangan shahri', 'намангана', 'намангане', 'намангану'],
    'наманган': ['наманган', 'namangan', 'namanganga', 'namangandan', 'namanganda', 
                'namangan shahri', 'намангана', 'намангане', 'намангану'],
    
    # === FERGANA / ФЕРГАНА ===
    'fargona': ['фергана', 'fargona', 'fergana', 'farghona', 'farg'ona', 'fargonaга', 
               'fargonadan', 'fargonada', 'fargona shahri', 'ферганы', 'фергане', 'фергану'],
    'fergana': ['фергана', 'fargona', 'fergana', 'farghona', 'farg'ona', 'fargonaга', 
               'fargonadan', 'fargonada', 'fargona shahri', 'ферганы', 'фергане', 'фергану'],
    'фергана': ['фергана', 'fargona', 'fergana', 'farghona', 'farg'ona', 'fargonaга', 
               'fargonadan', 'fargonada', 'fargona shahri', 'ферганы', 'фергане', 'фергану'],
    
    # === ANDIJAN / АНДИЖАН ===
    'andijon': ['андижан', 'andijon', 'andijan', 'andizhon', 'andijonга', 'andijondan', 
               'andijonda', 'andijon shahri', 'андижана', 'андижане', 'андижану'],
    'andijan': ['андижан', 'andijon', 'andijan', 'andizhon', 'andijonга', 'andijondan', 
               'andijonda', 'andijon shahri', 'андижана', 'андижане', 'андижану'],
    'андижан': ['андижан', 'andijon', 'andijan', 'andizhon', 'andijonга', 'andijondan', 
               'andijonda', 'andijon shahri', 'андижана', 'андижане', 'андижану'],
    
    # === BUKHARA / БУХАРА ===
    'buxoro': ['бухара', 'buxoro', 'bukhara', 'buchara', 'buxoroga', 'buxorodan', 
              'buxoroda', 'buxoro shahri', 'бухары', 'бухаре', 'бухару'],
    'bukhara': ['бухара', 'buxoro', 'bukhara', 'buchara', 'buxoroga', 'buxorodan', 
               'buxoroda', 'buxoro shahri', 'бухары', 'бухаре', 'бухару'],
    'бухара': ['бухара', 'buxoro', 'bukhara', 'buchara', 'buxoroga', 'buxorodan', 
              'buxoroda', 'buxoro shahri', 'бухары', 'бухаре', 'бухару'],
    
    # === NUKUS / НУКУС ===
    'nukus': ['нукус', 'nukus', 'no'kis', "no'kis", 'nukusga', 'nukusdan', 'nukusda', 
             'nukus shahri', 'нукуса', 'нукусе', 'нукусу'],
    'нукус': ['нукус', 'nukus', 'no'kis', "no'kis", 'nukusga', 'nukusdan', 'nukusda', 
             'nukus shahri', 'нукуса', 'нукусе', 'нукусу'],
    
    # === URGENCH / УРГЕНЧ ===
    'urganch': ['ургенч', 'urganch', 'urgench', 'urgancha', 'urganchga', 'urganchdan', 
               'urganchda', 'urganch shahri', 'ургенча', 'ургенче', 'ургенчу'],
    'urgench': ['ургенч', 'urganch', 'urgench', 'urgancha', 'urganchga', 'urganchdan', 
               'urganchda', 'urganch shahri', 'ургенча', 'ургенче', 'ургенчу'],
    'ургенч': ['ургенч', 'urganch', 'urgench', 'urgancha', 'urganchga', 'urganchdan', 
              'urganchda', 'urganch shahri', 'ургенча', 'ургенче', 'ургенчу'],
    
    # === KHIVA / ХИВА ===
    'xiva': ['хива', 'xiva', 'khiva', 'hiva', 'xivaga', 'xivadan', 'xivada', 
            'xiva shahri', 'хивы', 'хиве', 'хиву'],
    'khiva': ['хива', 'xiva', 'khiva', 'hiva', 'xivaga', 'xivadan', 'xivada', 
             'xiva shahri', 'хивы', 'хиве', 'хиву'],
    'хива': ['хива', 'xiva', 'khiva', 'hiva', 'xivaga', 'xivadan', 'xivada', 
            'xiva shahri', 'хивы', 'хиве', 'хиву'],
    
    # === QARSHI / КАРШИ ===
    'qarshi': ['карши', 'qarshi', 'karshi', 'qarshiga', 'qarshidan', 'qarshida', 
              'qarshi shahri', 'карши', 'карше', 'каршу'],
    'карши': ['карши', 'qarshi', 'karshi', 'qarshiga', 'qarshidan', 'qarshida', 
             'qarshi shahri', 'карши', 'карше', 'каршу'],
    
    # === TERMEZ / ТЕРМЕЗ ===
    'termiz': ['термез', 'termiz', 'termez', 'termizga', 'termizdan', 'termizda', 
              'termiz shahri', 'термеза', 'термезе', 'термезу'],
    'termez': ['термез', 'termiz', 'termez', 'termizga', 'termizdan', 'termizda', 
              'termiz shahri', 'термеза', 'термезе', 'термезу'],
    'термез': ['термез', 'termiz', 'termez', 'termizga', 'termizdan', 'termizda', 
              'termiz shahri', 'термеза', 'термезе', 'термезу'],
    
    # === KOKAND / КОКАН ===
    'qoqon': ['кокан', 'qoqon', 'kokand', 'kokan', 'qoqonga', 'qoqondan', 'qoqonda', 
             'qoqon shahri', 'кокана', 'кокане', 'кокану'],
    'kokand': ['кокан', 'qoqon', 'kokand', 'kokan', 'qoqonga', 'qoqondan', 'qoqonda', 
              'qoqon shahri', 'кокана', 'кокане', 'кокану'],
    'кокан': ['кокан', 'qoqon', 'kokand', 'kokan', 'qoqonga', 'qoqondan', 'qoqonda', 
             'qoqon shahri', 'кокана', 'кокане', 'кокану'],
    
    # === NAVOIY / НАВОИ ===
    'navoiy': ['навои', 'navoiy', 'navoi', 'navoiyga', 'navoiydan', 'navoiyda', 
              'navoiy shahri', 'навои', 'навое', 'навою'],
    'navoi': ['навои', 'navoiy', 'navoi', 'navoiyga', 'navoiydan', 'navoiyda', 
             'navoiy shahri', 'навои', 'навое', 'навою'],
    'навои': ['навои', 'navoiy', 'navoi', 'navoiyga', 'navoiydan', 'navoiyda', 
             'navoiy shahri', 'навои', 'навое', 'навою'],
    
    # === GULISTAN / ГУЛИСТАН ===
    'guliston': ['гулистан', 'guliston', 'gulistan', 'gulistonga', 'gulistondan', 'gulistonda', 
                'guliston shahri', 'гулистана', 'гулистане', 'гулистану'],
    'gulistan': ['гулистан', 'guliston', 'gulistan', 'gulistonga', 'gulistondan', 'gulistonda', 
                'guliston shahri', 'гулистана', 'гулистане', 'гулистану'],
    'гулистан': ['гулистан', 'guliston', 'gulistan', 'gulistonga', 'gulistondan', 'gulistonda', 
                'guliston shahri', 'гулистана', 'гулистане', 'гулистану'],
    
    # === ANGREN / АНГРЕН ===
    'angren': ['ангрен', 'angren', 'angiren', 'angrеnga', 'angrendan', 'angrenda', 
              'angren shahri', 'ангрена', 'ангрене', 'ангрену'],
    'ангрен': ['ангрен', 'angren', 'angiren', 'angrеnga', 'angrendan', 'angrenda', 
              'angren shahri', 'ангрена', 'ангрене', 'ангрену'],
    
    # === ALMALYK / АЛМАЛЫК ===
    'olmaliq': ['алмалык', 'olmaliq', 'almalyk', 'almalik', 'olmalik', 'olmaliqga', 
               'olmaliqdan', 'olmaliqda', 'olmaliq shahri', 'алмалыка', 'алмалыке', 'алмалыку'],
    'almalyk': ['алмалык', 'olmaliq', 'almalyk', 'almalik', 'olmalik', 'olmaliqga', 
               'olmaliqdan', 'olmaliqda', 'olmaliq shahri', 'алмалыка', 'алмалыке', 'алмалыку'],
    'алмалык': ['алмалык', 'olmaliq', 'almalyk', 'almalik', 'olmalik', 'olmaliqga', 
               'olmaliqdan', 'olmaliqda', 'olmaliq shahri', 'алмалыка', 'алмалыке', 'алмалыку'],
    
    # === BEKABAD / БЕКАБАД ===
    'bekobod': ['бекабад', 'bekobod', 'bekabad', 'bekobodga', 'bekoboddan', 'bekobodda', 
               'bekobod shahri', 'бекабада', 'бекабаде', 'бекабаду'],
    'bekabad': ['бекабад', 'bekobod', 'bekabad', 'bekobodga', 'bekoboddan', 'bekobodda', 
               'bekobod shahri', 'бекабада', 'бекабаде', 'бекабаду'],
    'бекабад': ['бекабад', 'bekobod', 'bekabad', 'bekobodga', 'bekoboddan', 'bekobodda', 
               'bekobod shahri', 'бекабада', 'бекабаде', 'бекабаду'],
    
    # === YANGIYUL / ЯНГИЮЛЬ ===
    'yangiyul': ['янгиюль', 'yangiyul', 'yangiyo\'l', 'yangiyulik', 'yangiyulga', 
                'yangiyuldan', 'yangiyulda', 'yangiyul shahri', 'янгиюля', 'янгиюле', 'янгиюлю'],
    'янгиюль': ['янгиюль', 'yangiyul', 'yangiyo\'l', 'yangiyulik', 'yangiyulga', 
               'yangiyuldan', 'yangiyulda', 'yangiyul shahri', 'янгиюля', 'янгиюле', 'янгиюлю'],
    
    # === CHIRCHIK / ЧИРЧИК ===
    'chirchiq': ['чирчик', 'chirchiq', 'chirchik', 'chirchiqqa', 'chirchiqdan', 'chirchiqda', 
                'chirchiq shahri', 'чирчика', 'чирчике', 'чирчику'],
    'chirchik': ['чирчик', 'chirchiq', 'chirchik', 'chirchiqqa', 'chirchiqdan', 'chirchiqda', 
                'chirchiq shahri', 'чирчика', 'чирчике', 'чирчику'],
    'чирчик': ['чирчик', 'chirchiq', 'chirchik', 'chirchiqqa', 'chirchiqdan', 'chirchiqda', 
              'chirchiq shahri', 'чирчика', 'чирчике', 'чирчику'],
    
    # === CHINAZ / ЧИНАЗ ===
    'chinoz': ['чиназ', 'chinoz', 'chinaz', 'chinozga', 'chinozdan', 'chinozda', 
              'chinoz shahri', 'чиназа', 'чиназе', 'чиназу'],
    'chinaz': ['чиназ', 'chinoz', 'chinaz', 'chinozga', 'chinozdan', 'chinozda', 
              'chinoz shahri', 'чиназа', 'чиназе', 'чиназу'],
    'чиназ': ['чиназ', 'chinoz', 'chinaz', 'chinozga', 'chinozdan', 'chinozda', 
             'chinoz shahri', 'чиназа', 'чиназе', 'чиназу'],
    
    # === INTERNATIONAL CITIES ===
    
    # MOSCOW
    'moskva': ['москва', 'moskva', 'moscow', 'moskau', 'moskow', 'moskvaga', 'moskvadan', 
              'moskvada', 'московский', 'москвы', 'москве', 'москву', 'московской'],
    'moscow': ['москва', 'moskva', 'moscow', 'moskau', 'moskow', 'moskvaga', 'moskvadan', 
              'moskvada', 'московский', 'москвы', 'москве', 'москву', 'московской'],
    'москва': ['москва', 'moskva', 'moscow', 'moskau', 'moskow', 'moskvaga', 'moskvadan', 
              'moskvada', 'московский', 'москвы', 'москве', 'москву', 'московской'],
    
    # ALMATY
    'almaty': ['алматы', 'almaty', 'olmata', 'almata', 'алма-ата', 'alma-ata', 'almatyga', 
              'almatydan', 'almatyda', 'алматинский', 'алматы', 'алмате', 'алмату'],
    'olmata': ['алматы', 'almaty', 'olmata', 'almata', 'алма-ата', 'alma-ata', 'almatyga', 
              'almatydan', 'almatyda', 'алматинский', 'алматы', 'алмате', 'алмату'],
    'алматы': ['алматы', 'almaty', 'olmata', 'almata', 'алма-ата', 'alma-ata', 'almatyga', 
              'almatydan', 'almatyda', 'алматинский', 'алматы', 'алмате', 'алмату'],
    
    # ASTANA
    'astana': ['астана', 'astana', 'nur-sultan', 'нур-султан', 'astanaga', 'astanadan', 
              'astanada', 'астаны', 'астане', 'астану'],
    'астана': ['астана', 'astana', 'nur-sultan', 'нур-султан', 'astanaga', 'astanadan', 
              'astanada', 'астаны', 'астане', 'астану'],
    
    # ISTANBUL
    'istanbul': ['стамбул', 'istanbul', 'İstanbul', 'constantinople', 'constantinopol', 
                'istanbulga', 'istanbuldan', 'istanbulda', 'стамбула', 'стамбуле', 'стамбулу'],
    'стамбул': ['стамбул', 'istanbul', 'İstanbul', 'constantinople', 'constantinopol', 
               'istanbulga', 'istanbuldan', 'istanbulda', 'стамбула', 'стамбуле', 'стамбулу'],
    
    # ANKARA
    'ankara': ['анкара', 'ankara', 'angara', 'ankaraga', 'ankaradan', 'ankarada', 
              'анкары', 'анкаре', 'анкару'],
    'анкара': ['анкара', 'ankara', 'angara', 'ankaraga', 'ankaradan', 'ankarada', 
              'анкары', 'анкаре', 'анкару'],
    
    # GROZNY
    'grozny': ['грозный', 'grozny', 'groznyy', 'grozniy', 'groznyga', 'groznydan', 
              'groznyda', 'грозного', 'грозном', 'грозному'],
    'грозный': ['грозный', 'grozny', 'groznyy', 'grozniy', 'groznyga', 'groznydan', 
               'groznyda', 'грозного', 'грозном', 'грозному'],
    
    # Additional cities with special characters and grammatical forms
    'şymkent': ['шымкент', 'şymkent', 'shymkent', 'chimkent', 'шымкента', 'шымкенте', 'шымкенту'],
    'şymkentga': ['шымкент', 'şymkent', 'shymkent', 'chimkent'],
    
    # KHOREZM region variants
    'xorazm': ['хорезм', 'xorazm', 'khorezm', 'chorezm', 'хоразм', 'xorizmga', 'xorizmdan'],
    'хорезм': ['хорезм', 'xorazm', 'khorezm', 'chorezm', 'хоразм', 'xorizmga', 'xorizmdan'],
    
    # Special case: Khorezm region center (often confused)
    'xorziga': ['хорзига', 'xorziga', 'khorezm center', 'хоразм центр'],
    'хорзига': ['хорзига', 'xorziga', 'khorezm center', 'хоразм центр'],
}

def get_city_variants(city_name):
    """
    Get all possible variants for a city name
    Returns a list of all possible spellings and grammatical forms
    """
    city_clean = city_name.lower().strip()
    
    # Direct lookup
    if city_clean in CITY_VARIANTS:
        return CITY_VARIANTS[city_clean]
    
    # Fallback: check if city_name is in any of the variant lists
    for key, variants in CITY_VARIANTS.items():
        if city_clean in [v.lower() for v in variants]:
            return variants
            
    # If no match found, return the original city name
    return [city_clean]

def normalize_city_name(city_name):
    """
    Normalize city name to its primary form
    """
    variants = get_city_variants(city_name)
    return variants[0] if variants else city_name.lower()
