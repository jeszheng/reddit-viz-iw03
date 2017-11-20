gov = ['.gov']
fox = ['fox']
academic_professional = ['.edu', '.ieee']
video = ['youtube.com', 'vimeo']
social_media = ['reddit.com']
digital_media = ['buzzfeed', 'go.com', 'yahoo', 'mashable']
non_profit = ['.org', 'commondreams']
political_journal = [   'conservative',
                        'fivethirtyeight',
                        'politi',
                        'nationalreview',
                        'redstate',
                        'rightwingwatch',
                        'reason.com',
                        'shareblue',
                        'talkingpointsmemo.com',
                        'thehill.com',
                        'thenation',
                        'washingtonexaminer',
                        ]
magazine = [            'chronicle',
                        'economist',
                        'esquire',
                        'fortune',
                        'forbes',
                        'gq',
                        'hollywood',
                        'instyle',
                        'magazine',
                        'motherjones',
                        'nationalgeographic',
                        'newrepublic',
                        'newyorker',
                        'nymag',
                        'people',
                        'rollingstone',
                        'slate',
                        'smithsonianmag',
                        'teenvogue',
                        'theatlantic',
                        'thefederalist',
                        'time.com',
                        'vanityfair',
                        'vice',
                        'vulture'
                        ]

tech = [                'android',
                        'arstechnica',
                        'bleepingcomputer',
                        'bot',
                        'byte',
                        'cleantechnica',
                        'cnet',
                        'digitaltrends',
                        'dslreports',
                        'electr',
                        'engadget',
                        'engineering',
                        'geekwire',
                        'gizmodo',
                        'hackread',
                        'hardware',
                        'inverse',
                        'newatlas',
                        'newscientist',
                        'privateinternetaccess',
                        'pcmag',
                        'popularmechanics',
                        'recode',
                        'science',
                        'scientificamerican',
                        'silicon',
                        'tech',
                        'thehackernews',
                        'thenextweb',
                        'theinquirer',
                        'torrentfreak',
                        'venturebeat',
                        'wired',
                        'zdnet'
                        ]
blog_opinion = [        'axios',
                        'climatechangenews',
                        'huffingtonpost',
                        'lawfareblog',
                        'medium.com',
                        'nypost',
                        'salon.com',
                        'theconversation',
                        'theverge',
                        'vox'
                        ]
international = [       '.au',
                        '.ca',
                        '.cn',
                        '.co.kr',
                        '.co.nz',
                        '.co.uk',
                        '.de',
                        '.dk',
                        '.eu',
                        '.fr',
                        '.lb',
                        '.ie',
                        '.ir',
                        '.in',
                        '.it',
                        '.jp',
                        '.va',
                        '.na',
                        '.se',
                        'aljazeera',
                        'albawaba',
                        'arab',
                        'bbc',
                        'bbc',
                        'cbc.ca',
                        'chinadaily',
                        'colombia',
                        'co.jp',
                        'dw.com',
                        'euronews',
                        'foreignpolicy',
                        'france',
                        'haaretz',
                        'hindu',
                        'irishtimes',
                        'india',
                        'japantimes',
                        'jpost',
                        'middleeast',
                        'nationalpost.com',
                        'rt.com',
                        'russia',
                        'sputniknews',
                        'telesurtv',
                        'theguardian',
                        'themoscowtimes',
                        'thestar',
                        'theweek',
                        'timesofisrael',
                        'xinhuanet'
                        ]
american_news = [       'abc',
                        'apnews',
                        'baltimoresun',
                        'blade',
                        'bloomberg',
                        'bostonglobe',
                        'businessinsider.com',
                        'cbslocal',
                        'cbsnews',
                        'chicago',
                        'detroit',
                        'cleveland',
                        'city',
                        'cnbc',
                        'cnn',
                        'colorado',
                        'ctvnews',
                        'daily',
                        'denver',
                        'gazette',
                        'herald',
                        'ibtimes.com',
                        'ktla',
                        'lasvegas',
                        'latimes',
                        'lawnewz',
                        'live',
                        'jersey',
                        'marketwatch',
                        'miamiherald',
                        'msnbc',
                        'msn.com',
                        'nbc',
                        'new',
                        'news3lv',
                        'newsmax',
                        'newsweek',
                        'nj.com',
                        'nydailynews',
                        'nytimes',
                        'oregon',
                        'philly',
                        'pbs',
                        'qz',
                        'reuters',
                        'richmond.com',
                        'sentinel',
                        'sfgate',
                        'star',
                        'tampabay',
                        'theadvocate',
                        'thedailybeast',
                        'theintercept',
                        'thinkprogress',
                        'today',
                        'times',
                        'tribune',
                        'usatoday',
                        'washington',
                        'wsj',
                        'weekly'
                        ]

def contains_domain(domain, set_of_options):
    for option in set_of_options:
        if option in domain:
            return True
    return False

def categorize(list_of_domains):
    categories = {}
    categories['gov'] = 0
    categories['fox'] = 0
    categories['academic_professional'] = 0
    categories['video'] = 0
    categories['social_media'] = 0
    categories['digital_media'] = 0
    categories['non_profit'] = 0
    categories['political_journal'] = 0
    categories['tech'] = 0
    categories['magazine'] = 0
    categories['blog_opinion'] = 0
    categories['international'] = 0
    categories['american_news'] = 0
    categories['local_news'] = 0
    categories['other'] = 0
    categories['total'] = 0

    for domain in list_of_domains:
        categories['total'] += 1
        if contains_domain(domain, gov):
            categories['gov'] += 1
        elif contains_domain(domain, fox):
            categories['fox'] += 1
        elif contains_domain(domain, academic_professional):
            categories['academic_professional'] += 1
        elif contains_domain(domain, video):
            categories['video'] += 1
        elif contains_domain(domain, social_media):
            categories['social_media'] += 1
        elif contains_domain(domain, digital_media):
            categories['digital_media'] += 1
        # local news channels.
        elif ((len(domain) == 8) and (domain[-4:] == '.com')):
            categories['local_news'] += 1
        elif contains_domain(domain, non_profit):
            categories['non_profit'] += 1
        elif contains_domain(domain, political_journal):
            categories['political_journal'] += 1
        elif contains_domain(domain, magazine):
            categories['magazine'] += 1
        elif contains_domain(domain, tech):
            categories['tech'] += 1
        elif contains_domain(domain, blog_opinion):
            categories['blog_opinion'] += 1
        elif contains_domain(domain, international):
            categories['international'] += 1
        elif contains_domain(domain, american_news):
            categories['american_news'] += 1
        else:
            categories['other'] += 1
    return categories
