
flag_emojis = [':flag-ch:',':flag-iq:',':flag-ng:',':flag-nl:',':flag-vn:',':uk:',':flag-kw:',':flag-us:',':flag-za:',
':flag-br:',':flag-jp:',':flag-de:',':flag-bd:',':flag-id:',':fr:',':it:',':flag-qa:',':flag-sg:',':flag-om:',
':flag-lk:',':flag-sa:',':flag-kr:',':flag-np:',':flag-cn:',':flag-au:',':flag-my:',':flag-hk:',':flag-tr:',':ru:',
':flag-be:',':flag-ae:',':flag-th:']

flag_countries = [
    'Switzerland',
    'Iraq',
    'Nigeria',
    'Netherlands',
    'Vietnam',
    'United Kingdom',
    'Kuwait',
    'United States',
    'South Africa',
    'Brazil',
    'Japan',
    'Germany',
    'Bangladesh',
    'Indonesia',
    'France',
    'Italy',
    'Qatar',
    'Singapore',
    'Oman',
    'Sri Lanka',
    'Saudi Arabia',
    'Korea',
    'Nepal',
    'China',
    'Australia',
    'Malaysia',
    'Hong Kong SAR',
    'Türkiye',
    'Russia',
    'Belgium',
    'United Arab Emirates',
    'Thailand'
]

def get_flag_dict():
    return dict(zip(flag_countries, flag_emojis))