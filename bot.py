import sqlite3
import random
import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
)
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage

BOT_TOKEN = "8936967784:AAGN6zqBLcbcazP89e4RClwJuLVy6nLCstM"

COUNTRY_FLAGS = {
    "France": "🇫🇷",
    "Germany": "🇩🇪",
    "Spain": "🇪🇸",
    "Italy": "🇮🇹",
    "England": "🏴󠁧󠁢󠁥󠁮󠁧󠁿",
    "Brazil": "🇧🇷",
    "Argentina": "🇦🇷",
    "Portugal": "🇵🇹",
    "Netherlands": "🇳🇱",
    "Belgium": "🇧🇪",
    "Croatia": "🇭🇷",
    "Poland": "🇵🇱",
    "Colombia": "🇨🇴",
    "Uruguay": "🇺🇾",
    "United States": "🇺🇸",
    "Japan": "🇯🇵",
    "Korea, South": "🇰🇷",
    "Austria": "🇦🇹",
    "Switzerland": "🇨🇭",
    "Denmark": "🇩🇰",
    "Sweden": "🇸🇪",
    "Norway": "🇳🇴",
    "Serbia": "🇷🇸",
    "Ukraine": "🇺🇦",
    "Turkey": "🇹🇷",
    "Scotland": "🏴󠁧󠁢󠁳󠁣󠁴󠁿",
    "Mexico": "🇲🇽",
    "Canada": "🇨🇦",
    "Wales": "🏴󠁧󠁢󠁷󠁬󠁳󠁿",
    "Morocco": "🇲🇦",
    "Senegal": "🇸🇳",
    "Algeria": "🇩🇿",
    "Ghana": "🇬🇭",
    "Cameroon": "🇨🇲",
    "Nigeria": "🇳🇬",
    "Ivory Coast": "🇨🇮",
    "Egypt": "🇪🇬",
    "Mali": "🇲🇱",
    "Tunisia": "🇹🇳",
    "Australia": "🇦🇺",
    "Iran": "🇮🇷",
    "Saudi Arabia": "🇸🇦",
    "Ecuador": "🇪🇨",
    "Peru": "🇵🇪",
    "Chile": "🇨🇱",
    "Paraguay": "🇵🇾",
    "Venezuela": "🇻🇪",
    "Bolivia": "🇧🇴",
    "Bosnia-Herzegovina": "🇧🇦",
    "Czech Republic": "🇨🇿",
    "Slovakia": "🇸🇰",
    "Hungary": "🇭🇺",
    "Romania": "🇷🇴",
    "Bulgaria": "🇧🇬",
    "Greece": "🇬🇷",
    "Finland": "🇫🇮",
    "Ireland": "🇮🇪",
    "Northern Ireland": "🇬🇧",
    "Iceland": "🇮🇸",
    "Slovenia": "🇸🇮",
    "Albania": "🇦🇱",
    "North Macedonia": "🇲🇰",
    "Montenegro": "🇲🇪",
    "Georgia": "🇬🇪",
}

POSITIONS_RU = {
    "Goalkeeper": "🧤 Вратарь",
    "Centre-Back": "🧱 ЦЗ",
    "Left-Back": "⬅️ ЛЗ",
    "Right-Back": "➡️ ПЗ",
    "Defensive Midfield": "🛡 Опорник",
    "Central Midfield": "⚙️ ЦП",
    "Attacking Midfield": "🎯 ЦАП",
    "Right Midfield": "➡️ ПП",
    "Left Midfield": "⬅️ ЛП",
    "Left Winger": "🏃 ЛВ",
    "Right Winger": "🏃 ПВ",
    "Centre-Forward": "⚽ Нападающий",
    "Second Striker": "🎭 Оттянутый форвард",
    "Midfield": "⚙️ Полузащитник",
    "Attack": "⚽ Нападение",
    "Defender": "🧱 Защитник",
}

RU_COUNTRIES = {
    "France": ["франция", "францию"],
    "Germany": ["германия", "германию", "фрг"],
    "Spain": ["испания", "испанию"],
    "Italy": ["италия", "италию"],
    "England": ["англия", "англию"],
    "Brazil": ["бразилия", "бразилию"],
    "Argentina": ["аргентина", "аргентину"],
    "Portugal": ["португалия", "португалию"],
    "Netherlands": ["нидерланды", "голандия", "голландия", "голандию", "голландию"],
    "Belgium": ["бельгия", "бельгию"],
    "Croatia": ["хорватия", "хорватию"],
    "Poland": ["польша", "польшу"],
    "Colombia": ["колумбия", "колумбию"],
    "Uruguay": ["уругвай"],
    "Japan": ["япония", "японию"],
    "Serbia": ["сербия", "сербию"],
    "Ukraine": ["украина", "украину"],
    "Turkey": ["турция", "турцию"],
    "Mexico": ["мексика", "мексику"],
    "United States": ["сша", "америка", "америку"],
    "Canada": ["канада", "канаду"],
    "Denmark": ["дания", "данию"],
    "Switzerland": ["швейцария", "швейцарию"],
    "Scotland": ["шотландия", "шотландию"],
    "Wales": ["уэльс"],
    "Morocco": ["марокко"],
    "Senegal": ["сенегал"],
    "Ghana": ["гана", "гану"],
    "Cameroon": ["камерун"],
    "Nigeria": ["нигерия", "нигерию"],
    "Ivory Coast": ["кот дивуар", "кот-д'ивуар"],
    "Egypt": ["египет"],
    "Mali": ["мали"],
    "Tunisia": ["тунис"],
    "Algeria": ["алжир"],
    "South Korea": ["южная корея", "корея"],
    "Korea, South": ["южная корея", "корея"],
    "Australia": ["австралия", "австралию"],
    "Iran": ["иран"],
    "Saudi Arabia": ["саудовская аравия", "саудовскую аравию"],
    "Ecuador": ["эквадор"],
    "Peru": ["перу"],
    "Chile": ["чили"],
    "Paraguay": ["парагвай"],
    "Venezuela": ["венесуэла", "венесуэлу"],
    "Bolivia": ["боливия", "боливию"],
    "Bosnia-Herzegovina": ["босния", "босния и герцеговина"],
    "Austria": ["австрия", "австрию"],
    "Sweden": ["швеция", "швецию"],
    "Norway": ["норвегия", "норвегию"],
    "Czech Republic": ["чехия", "чехию"],
    "Slovakia": ["словакия", "словакию"],
    "Hungary": ["венгрия", "венгрию"],
    "Romania": ["румыния", "румынию"],
    "Bulgaria": ["болгария", "болгарию"],
    "Greece": ["греция", "грецию"],
    "Finland": ["финляндия", "финляндию"],
    "Ireland": ["ирландия", "ирландию"],
    "Northern Ireland": ["северная ирландия"],
    "Iceland": ["исландия", "исландию"],
    "Slovenia": ["словения", "словению"],
    "Albania": ["албания", "албанию"],
    "North Macedonia": ["северная македония", "македония"],
    "Montenegro": ["черногория", "черногорию"],
    "Georgia": ["грузия", "грузию"],
}

RU_CLUBS = {
    # === АПЛ И ЧЕМПИОНШИП ===
    "Arsenal Football Club": ["арсенал", "арсенал лондон"],
    "Manchester City Football Club": ["манчестер сити", "ман сити", "сити"],
    "Manchester United Football Club": ["манчестер юнайтед", "мю", "м ю"],
    "Chelsea Football Club": ["челси"],
    "Liverpool Football Club": ["ливерпуль", "ливер"],
    "Tottenham Hotspur Football Club": ["тоттенхэм", "шпоры"],
    "Everton Football Club": ["эвертон"],
    "Aston Villa Football Club": ["астон вилла", "вилла"],
    "Newcastle United Football Club": ["ньюкасл", "ньюкасл юнайтед"],
    "West Ham United Football Club": ["вест хэм", "вестхем"],
    "Crystal Palace Football Club": ["кристал пэлас", "пэлас"],
    "Fulham Football Club": ["фулхэм", "фулем"],
    "Brighton and Hove Albion Football Club": ["брайтон"],
    "Association Football Club Bournemouth": ["борнмут"],
    "Nottingham Forest Football Club": ["ноттингем", "ноттингем форест"],
    "Wolverhampton Wanderers Football Club": ["вулверхэмптон", "вулвз", "волки"],
    "Sheffield United Football Club": ["шеффилд", "шеффилд юнайтед"],
    "Luton Town Football Club": ["лутон", "лутон таун"],
    "Burnley Football Club": ["бернли"],
    "Sunderland Association Football Club": ["сандерленд"],
    "Leicester City": ["лестер", "лестер сити"],
    "Southampton FC": ["саутгемптон"],
    "Leeds United": ["лидс", "лидс юнайтед"],
    "Stoke City": ["сток сити", "сток"],
    "Queens Park Rangers": ["кпр", "куинз парк рейнджерс"],
    "West Bromwich Albion": ["вест бромвич", "вест бром"],
    "Swansea City": ["суонси", "суонси сити"],
    "Hull City": ["халл сити", "халл"],
    "Middlesbrough FC": ["мидлсбро"],
    "Watford FC": ["уотфорд"],
    "Cardiff City": ["кардифф", "кардифф сити"],
    "Norwich City": ["норвич", "норвич сити"],
    "Reading FC": ["рединг"],
    "Wigan Athletic": ["уиган", "уиган атлетик"],
    "Blackburn Rovers": ["блэкберн", "блэкберн роверс"],
    "Bolton Wanderers": ["болтон", "болтон уондерерс"],
    "Charlton Athletic": ["чарльтон", "чарльтон атлетик"],
    "Brentford FC": ["брентфорд"],
    # === ЛА ЛИГА ===
    "Real Madrid": ["реал", "реал мадрид"],
    "Futbol Club Barcelona": ["барселона", "барса"],
    "Club Atlético de Madrid S.A.D.": ["атлетико", "атлетико мадрид"],
    "Sevilla FC": ["севилья"],
    "Real Sociedad de Fútbol S.A.D.": ["реал сосьедад", "сосьедад"],
    "Villarreal Club de Fútbol S.A.D.": ["вильярреал", "вильяреал"],
    "Real Betis Balompié S.A.D.": ["бетис", "реал бетис"],
    "Athletic Club Bilbao": ["атлетик", "атлетик бильбао"],
    "Valencia Club de Fútbol S. A. D.": ["валенсия"],
    "Club Atlético Osasuna": ["осасуна"],
    "Deportivo Alavés S. A. D.": ["алавес"],
    "UD Las Palmas": ["лас-пальмас", "лас пальмас"],
    "Real Club Deportivo Mallorca S.A.D.": ["мальорка", "майорка"],
    "Real Club Celta de Vigo S. A. D.": ["сельта", "сельта виго"],
    "Getafe Club de Fútbol S. A. D.": ["хетафе"],
    "Cádiz CF": ["кадис"],
    "Granada CF": ["гранада"],
    "Rayo Vallecano de Madrid S. A. D.": ["райо вальекано", "райо"],
    "UD Almería": ["альмерия"],
    "Girona Fútbol Club S. A. D.": ["жирона"],
    "Málaga CF": ["малага"],
    "Reial Club Deportiu Espanyol de Barcelona S.A.D.": ["эспаньол"],
    "Real Zaragoza": ["сарагоса", "реал сарагоса"],
    "Deportivo de La Coruña": ["депортиво", "депортиво ла-корунья"],
    "Levante Unión Deportiva S.A.D.": ["леванте"],
    "Elche Club de Fútbol S.A.D.": ["эльче"],
    "Real Valladolid CF": ["вальядолид", "реал вальядолид"],
    # === СЕРИЯ А ===
    "Juventus Football Club": ["ювентус", "юве"],
    "Associazione Calcio Milan": ["милан", "ас милан"],
    "Football Club Internazionale Milano S.p.A.": [
        "интер",
        "интернационале",
        "интер милан",
    ],
    "Società Sportiva Calcio Napoli": ["наполи"],
    "Associazione Sportiva Roma": ["рома"],
    "Società Sportiva Lazio S.p.A.": ["лацио"],
    "Atalanta Bergamasca Calcio S.p.a.": ["аталанта"],
    "Associazione Calcio Fiorentina": ["фиорентина", "фиалки"],
    "Bologna Football Club 1909": ["болонья"],
    "Torino Calcio": ["торино"],
    "Genoa Cricket and Football Club": ["дженоа"],
    "Unione Sportiva Sassuolo Calcio": ["сассуоло"],
    "Verona Hellas Football Club": ["верона", "эллас верона"],
    "Udinese Calcio": ["удинезе"],
    "Cagliari Calcio": ["кальяри"],
    "FC Empoli": ["эмполи"],
    "Frosinone Calcio": ["фрозиноне"],
    "US Salernitana 1919": ["салернитана"],
    "Parma Calcio 1913": ["парма"],
    "UC Sampdoria": ["сампдория"],
    "Delfino Pescara 1936": ["пескара"],
    "US Livorno 1915": ["ливорно"],
    "Chievo Verona": ["кьево"],
    "Brescia Calcio": ["брешия"],
    "Catania FC": ["катания"],
    "Calcio Como": ["комо"],
    "Cesena FC": ["чезена"],
    "US Lecce": ["лечче"],
    # === БУНДЕСЛИГА ===
    "FC Bayern München": ["бавария", "бавария мюнхен"],
    "Borussia Dortmund": ["боруссия д", "боруссия дортмунд", "дортмунд"],
    "RasenBallsport Leipzig": ["лейпциг", "рб лейпциг"],
    "Bayer 04 Leverkusen Fußball": ["байер", "байер 04", "байер леверкузен"],
    "Eintracht Frankfurt Fußball AG": ["айнтрахт", "айнтрахт ф", "айнтрахт франкфурт"],
    "Verein für Bewegungsspiele Stuttgart 1893": ["штутгарт"],
    "Sport-Club Freiburg": ["фрайбург"],
    "Turn- und Sportgemeinschaft 1899 Hoffenheim Fußball-Spielbetriebs": ["хоффенхайм"],
    "Sportverein Werder Bremen von 1899": ["вердер", "вердер бремен"],
    "1. FC Heidenheim 1846": ["хайденхайм"],
    "Fußball-Club Augsburg 1907": ["аугсбург"],
    "Verein für Leibesübungen Wolfsburg": ["вольфсбург"],
    "1. Fußball- und Sportverein Mainz 05": ["майнц", "майнц 05"],
    "VfL Bochum 1848": ["бохум"],
    "1. FC Union Berlin": ["унион", "унион берлин"],
    "Borussia Verein für Leibesübungen 1900 Mönchengladbach": [
        "боруссия м",
        "гладбах",
        "боруссия менхенгладбах",
    ],
    "1. Fußball-Club Köln": ["кёльн"],
    "SV Darmstadt 98": ["дармштадт", "дармштадт 98"],
    "FC Schalke 04": ["шальке", "шальке 04"],
    "Hertha BSC": ["герта", "герта берлин"],
    "Hamburger Sport Verein": ["гамбург"],
    "1.FC Nuremberg": ["нюрнберг"],
    "Hannover 96": ["ганновер", "ганновер 96"],
    "Eintracht Braunschweig": ["айнтрахт б", "айнтрахт брауншвейг"],
    "Fortuna Düsseldorf": ["фортуна", "фортуна д", "фортуна дюссельдорф"],
    "SC Paderborn 07": ["падерборн"],
    "SpVgg Greuther Fürth": ["гройтер фюрт"],
    # === ЛИГА 1 ===
    "Paris Saint-Germain Football Club": ["псж", "пари сен жермен", "пари сен-жермен"],
    "Olympique de Marseille": ["марсель", "олимпик марсель"],
    "Olympique Lyonnais": ["лион", "олимпик лион"],
    "Association sportive de Monaco Football Club": ["монако"],
    "Lille Olympique Sporting Club": ["лилль"],
    "Racing Club de Lens": ["ланс"],
    "Stade Rennais Football Club": ["ренн"],
    "Stade brestois 29": ["брест"],
    "Stade Reims": ["реймс"],
    "Toulouse Football Club": ["тулуза"],
    "Racing Club de Strasbourg Alsace": ["страсбур", "страсбург"],
    "Montpellier HSC": ["монпелье"],
    "Football Club de Nantes": ["нант"],
    "Football Club Lorient-Bretagne Sud": ["лорьян"],
    "Football Club de Metz": ["мец"],
    "Le Havre Athletic Club": ["гавр"],
    "Clermont Foot 63": ["клермон"],
    "Olympique Gymnaste Club Nice Côte d'Azur": ["ницца"],
    "AS Nancy-Lorraine": ["нанси"],
    "Thonon Évian Grand Genève FC": ["эвиан"],
    "SC Bastia": ["бастия"],
    "FC Sochaux-Montbéliard": ["сошо"],
    "Valenciennes FC": ["валансьен"],
    "GFC Ajaccio": ["аяччо", "газелек аяччо"],
    "AC Ajaccio": ["аяччо", "ас аяччо"],
    "ESTAC Troyes": ["труа"],
    "EA Guingamp": ["генгам"],
    "FC Girondins Bordeaux": ["бордо", "жиронден бордо"],
    "AS Saint-Étienne": ["сент-этьен", "сент этьен"],
    "SM Caen": ["кан"],
    "Angers Sporting Club de l'Ouest": ["анже"],
    "Dijon FCO": ["дижон"],
    # === КОРОТКИЕ КЛЮЧИ ДЛЯ УМНОГО ПОИСКА ПО ПОДСТРОКЕ ===
    "Arsenal": ["арсенал"],
    "Chelsea": ["челси"],
    "Liverpool": ["ливерпуль"],
    "Everton": ["эвертон"],
    "Fulham": ["фулхэм"],
    "Brentford": ["брентфорд"],
    "Burnley": ["бернли"],
    "Sevilla": ["севилья"],
    "Villarreal": ["вильярреал"],
    "Valencia": ["валенсия"],
    "Osasuna": ["осасуна"],
    "Mallorca": ["мальорка"],
    "Getafe": ["хетафе"],
    "Granada": ["гранада"],
    "Almería": ["альмерия"],
    "Girona": ["жирона"],
    "Málaga": ["малага"],
    "Zaragoza": ["сарагоса"],
    "Levante": ["леванте"],
    "Elche": ["эльче"],
    "Juventus": ["ювентус"],
    "Napoli": ["наполи"],
    "Roma": ["рома"],
    "Lazio": ["лацио"],
    "Atalanta": ["аталанта"],
    "Fiorentina": ["фиорентина"],
    "Bologna": ["болонья"],
    "Torino": ["торино"],
    "Genoa": ["дженоа"],
    "Sassuolo": ["сассуоло"],
    "Udinese": ["удинезе"],
    "Cagliari": ["кальяри"],
    "Empoli": ["эмполи"],
    "Frosinone Calcio": ["фрозиноне"],
    "Salernitana": ["салернитана"],
    "Parma": ["парма"],
    "Sampdoria": ["сампдория"],
    "Pescara": ["пескара"],
    "Livorno": ["ливорно"],
    "Brescia": ["брешия"],
    "Catania": ["катания"],
    "Cesena": ["чезена"],
    "Lecce": ["лечче"],
    "Dortmund": ["дортмунд", "боруссия д"],
    "Leipzig": ["лейпциг"],
    "Leverkusen": ["байер"],
    "Stuttgart": ["штутгарт"],
    "Freiburg": ["фрайбург"],
    "Hoffenheim": ["хоффенхайм"],
    "Heidenheim": ["хайденхайм"],
    "Augsburg": ["аугсбург"],
    "Wolfsburg": ["вольфсбург"],
    "Bochum": ["бохум"],
    "Darmstadt": ["дармштадт"],
    "Schalke": ["шальке"],
    "Nuremberg": ["нюрнберг"],
    "Nürnberg": ["нюрнберг"],
    "Hannover": ["ганновер"],
    "Paderborn": ["падерборн"],
    "Marseille": ["марсель"],
    "Monaco": ["монако"],
    "Lille": ["лилль"],
    "Lens": ["ланс"],
    "Rennes": ["ренн"],
    "Reims": ["реймс"],
    "Toulouse": ["тулуза"],
    "Strasbourg": ["страсбур"],
    "Montpellier": ["монпелье"],
    "Nantes": ["нант"],
    "Lorient": ["лорьян"],
    "Metz": ["мец"],
    "Clermont": ["клермон"],
    "Nice": ["ницца"],
    "Bastia": ["бастия"],
    "Sochaux": ["сошо"],
    "Valenciennes": ["валансьен"],
    "Ajaccio": ["аяччо"],
    "Troyes": ["труа"],
    "Guingamp": ["генгам"],
    "Bordeaux": ["бордо"],
    "Caen": ["кан"],
    "Angers": ["анже"],
    "Dijon": ["дижон"],
    "Real Sociedad": ["реал сосьедад"],
    "Real Betis": ["бетис"],
    "Celta de Vigo": ["сельта"],
    "Rayo Vallecano": ["райо вальекано"],
    "Inter Milan": ["интер"],
    "AC Milan": ["милан"],
    "Bayern München": ["бавария"],
    "Bayern Munich": ["бавария"],
    "Werder Bremen": ["вердер"],
    "Union Berlin": ["унион берлин"],
    "Paris Saint-Germain": ["псж"],
    "Saint-Étienne": ["сент-этьен"],
    "Athletic Club": ["атлетик"],
}

# === СЛОВАРЬ ИЗВЕСТНЫХ ИГРОКОВ И ЛЕГЕНД ДЛЯ РЕЖИМА КАРЬЕРЫ ===
# === СЛОВАРЬ ИЗВЕСТНЫХ ИГРОКОВ И ЛЕГЕНД ДЛЯ РЕЖИМА КАРЬЕРЫ ===
RU_PLAYERS = {
    # === УКРАИНСКИЕ ИГРОКИ ===
    "Andriy Shevchenko": ["шевченко", "андрей шевченко", "андрій шевченко"],
    "Andriy Yarmolenko": ["ярмоленко", "андрей ярмоленко", "андрій ярмоленко"],
    "Illia Zabarnyi": ["забарный", "илья забарный", "забарний", "ілля забарний"],
    "Oleksandr Zinchenko": ["зинченко", "александр зинченко", "олександр зінченко"],
    "Viktor Tsygankov": ["цыганков", "виктор цыганков", "віктор циганков", "циганков"],
    "Mykhaylo Mudryk": ["мудрик", "михаил мудрик", "михайло мудрик"],
    "Vitaliy Mykolenko": ["миколенко", "виталий миколенко", "віталій миколенко"],
    "Ruslan Malinovskyi": [
        "малиновский",
        "руслан малиновский",
        "руслан маліновський",
        "маліновський",
    ],
    "Artem Dovbyk": ["довбик", "артем довбик"],
    "Andriy Lunin": ["лунин", "андрей лунин", "лунін", "андрій лунін"],
    "Anatoliy Trubin": ["трубин", "анатолий трубин", "трубін", "анатолій трубін"],
    "Heorhiy Sudakov": ["судаков", "георгий судаков", "георгій судаков"],
    "Roman Yaremchuk": ["яремчук", "роман яремчук"],
    # === ЛЕГЕНДЫ И ИСТОРИЧЕСКИЕ ИГРОКИ ===
    "Ronaldo": ["роналдо", "зубастик"],
    "Zinedine Zidane": ["зидан", "зинедин зидан"],
    "Paolo Maldini": ["мальдини", "паоло мальдини"],
    "Francesco Totti": ["тотти", "франческо тотти"],
    "Alessandro Del Piero": ["дель пьеро", "алессандро дель пьеро"],
    "Luís Figo": ["фигу", "луис фигу"],
    "Rivaldo": ["ривалдо"],
    "Gabriel Batistuta": ["батистута", "габриэль батистута"],
    "Ruud van Nistelrooy": ["ван нистелрой", "руд ван нистелрой"],
    "Pavel Nedvěd": ["недвед", "павел недвед"],
    "Clarence Seedorf": ["зеедорф", "кларенс зеедорф"],
    "Dennis Bergkamp": ["бергкамп", "деннис бергкамп"],
    "Patrick Vieira": ["виейра", "патрик виейра"],
    "Roy Keane": ["кин", "рой кин"],
    "Paul Scholes": ["скоулз", "пол скоулз"],
    "Ryan Giggs": ["гиггз", "райан гиггз"],
    "Ronaldinho": ["роналдиньо", "роналдинью"],
    "Thierry Henry": ["анри", "тьерри анри"],
    "Didier Drogba": ["дрогба", "дидье дрогба"],
    "Samuel Eto'o": ["это'о", "самуэль это'о", "этоо"],
    "Petr Čech": ["чех", "петр чех"],
    "Nemanja Vidić": ["видич", "неманья видич"],
    "Carles Puyol": ["пуйоль", "карлес пуйоль"],
    "Roberto Carlos": ["роберто карлос", "карлос"],
    "Wayne Rooney": ["руни", "уэйн руни"],
    "Andrea Pirlo": ["пирло", "андреа пирло"],
    "David Beckham": ["бекхэм", "дэвид бекхэм", "бэкхем"],
    "Philipp Lahm": ["лам", "филипп лам"],
    "Bastian Schweinsteiger": ["швайнштайгер", "бастиан швайнштайгер"],
    "Miroslav Klose": ["клозе", "мирослав клозе"],
    "Steven Gerrard": ["джеррард", "стивен джеррард"],
    "Frank Lampard": ["лэмпард", "фрэнк лэмпард", "лампард"],
    "John Terry": ["терри", "джон терри"],
    "Rio Ferdinand": ["фердинанд", "рио фердинанд"],
    # === СОВРЕМЕННЫЕ ИГРОКИ (ТОП-УРОВЕНЬ) ===
    "Lionel Messi": ["месси", "лионель месси", "лео месси"],
    "Cristiano Ronaldo": ["роналду", "криштиану роналду", "криштиану", "криш"],
    "Zlatan Ibrahimović": ["ибрагимович", "златан ибрагимович", "златан", "ибра"],
    "Xavi": ["хави"],
    "Andrés Iniesta": ["иньеста", "андрес иньеста"],
    "Kaká": ["кака"],
    "Neymar": ["неймар", "неймар жуниор"],
    "Luis Suárez": ["суарес", "луис суарес"],
    "Karim Benzema": ["бензема", "карим бензема"],
    "Gareth Bale": ["бейл", "гарет бейл", "бэйл"],
    "Luka Modrić": ["модрич", "лука модрич"],
    "Toni Kroos": ["кроос", "тони кроос"],
    "Robert Lewandowski": ["левандовски", "роберт левандовски", "левандовский"],
    "Arjen Robben": ["роббен", "арьен роббен"],
    "Franck Ribéry": ["рибери", "франк рибери"],
    "Eden Hazard": ["азар", "эден азар"],
    "Sergio Ramos": ["рамос", "серхио рамос"],
    "Gerard Piqué": ["пике", "жерар пике"],
    "Manuel Neuer": ["нойер", "мануэль нойер"],
    "Gianluigi Buffon": ["буффон", "джанлуиджи буффон"],
    "Iker Casillas": ["касильяс", "икер касильяс"],
    "Thomas Müller": ["мюллер", "томас мюллер"],
    "Antoine Griezmann": ["гризманн", "антуан гризманн"],
    "Mohamed Salah": ["салах", "мохаммед салах"],
    "Harry Kane": ["кейн", "харри кейн", "гарри кейн"],
    "Kylian Mbappé": ["мбаппе", "килиан мбаппе"],
    "Erling Haaland": ["холанд", "эрлинг холанд", "холланд"],
    "Vinicius Júnior": ["винисиус", "вини", "винисиус жуниор"],
    "Jude Bellingham": ["беллингем", "джуд беллингем"],
    "Kevin De Bruyne": ["де брюйне", "кевин де брюйне"],
    "Sergio Agüero": ["агуэро", "серхио агуэро"],
    "David Silva": ["сильва", "давид сильва"],
    "Yaya Touré": ["яя туре", "туре"],
    "Cesc Fàbregas": ["фабрегас", "сеск фабрегас"],
    "Robin van Persie": ["ван перси", "робин ван перси"],
    "Angel Di María": ["ди мария", "анхель ди мария"],
    "Paul Pogba": ["погба", "поль погба"],
    "Romelu Lukaku": ["лукаку", "ромелу лукаку"],
    "Alexis Sánchez": ["санчес", "алексис санчес"],
    "Marco Reus": ["ройс", "марко ройс"],
    "Mats Hummels": ["хуммельс", "матс хуммельс"],
    "Raheem Sterling": ["стерлинг", "рахим стерлинг"],
    "Bruno Fernandes": ["фернандеш", "бруну фернандеш"],
    "Son Heung-min": ["сон", "сон хын мин"],
    "Thibaut Courtois": ["куртуа", "тибо куртуа"],
    "Virgil van Dijk": ["ван дейк", "вирджил ван дейк"],
    "Ruben Dias": ["диаш", "рубен диаш"],
    "Casemiro": ["каземиро"],
    "N'Golo Kanté": ["канте", "нголо канте"],
    "Sergio Busquets": ["бускетс", "серхио бускетс"],
    "James Rodríguez": ["родригес", "хамес родригес", "хамес"],
    "Pedri": ["педри"],
    "Jamal Musiala": ["мусиала", "джамал мусиала"],
    "Florian Wirtz": ["виртц", "вирц", "флориан виртц"],
    "Rodri": ["родри"],
    "Declan Rice": ["райс", "деклан райс"],
    "Martin Ødegaard": ["эдегор", "мартин эдегор"],
    "Bukayo Saka": ["сака", "букайо сака"],
    "Bernardo Silva": ["бернарду силва", "бернардо сильва"],
    "Lautaro Martínez": ["мартинес", "лаутаро мартинес"],
    "Paulo Dybala": ["дибала", "пауло дибала"],
    "Victor Osimhen": ["осимхен", "виктор осимхен"],
    "Khvicha Kvaratskhelia": ["кварацхелия", "хвича кварацхелия", "квара"],
    "Rafael Leão": ["леау", "рафаэл леау", "леао"],
    "Achraf Hakimi": ["хакими", "ашраф хакими"],
    "Alfonso Davies": ["девис", "альфонсо девис", "дэвис"],
    "Frenkie de Jong": ["де йонг", "френки де йонг"],
    "Federico Valverde": ["вальверде", "федерико вальверде"],
    "Ilkay Gündogan": ["гюндоган", "илкай гюндоган"],
    "Kai Havertz": ["хавертц", "кай хавертц", "хаверц"],
    "Leroy Sané": ["сане", "лерой сане"],
    "Marcelo": ["марсело"],
    "Dani Alves": ["дани алвес", "алвес"],
    "Sadio Mané": ["мане", "садио мане"],
    "Alisson": ["алиссон", "алисон"],
    "Ederson": ["эдерсон"],
    "Trent Alexander-Arnold": [
        "александер-арнольд",
        "трент",
        "трент александер-арнольд",
        "арнольд",
    ],
    "Roberto Firmino": ["фирмино", "роберто фирмино"],
    "João Félix": ["феликс", "жуан феликс", "жоау феликс"],
    "Enzo Fernández": ["энцо", "энцо фернандес", "фернандес"],
    "Gavi": ["гави"],
    "Lamine Yamal": ["ямаль", "ламин ямаль", "ямал"],
    "Ousmane Dembélé": ["дембеле", "усман дембеле"],
    "Olivier Giroud": ["жиру", "оливье жиру"],
    "Marcus Rashford": ["рэшфорд", "маркус рэшфорд"],
    "Phil Foden": ["фоден", "фил фоден"],
    "Jack Grealish": ["грилиш", "джек грилиш"],
    "Riyad Mahrez": ["марез", "рияд марез"],
    "Christian Eriksen": ["эриксен", "кристиан эриксен"],
    "Dries Mertens": ["мертенс", "дрис мертенс"],
    "Ciro Immobile": ["иммобиле", "чиро иммобиле"],
    "Edinson Cavani": ["кавани", "эдинсон кавани"],
    "Gonzalo Higuaín": ["игуаин", "гонсало игуаин"],
    "David de Gea": ["де хеа", "давид де хеа"],
    "Jan Oblak": ["облак", "ян облак"],
    "Marc-André ter Stegen": ["тер штеген", "марк-андре тер штеген"],
    "Emiliano Martínez": ["мартинес", "эмилиано мартинес", "эми мартинес"],
    "Thiago Silva": ["силва", "тиаго силва"],
    "Marquinhos": ["маркиньос"],
    "João Cancelo": ["канселу", "жуан канселу"],
}


def get_club_ru_display(club_en: str) -> str:
    if club_en in RU_CLUBS:
        return RU_CLUBS[club_en][0].title()

    club_lower = club_en.lower()
    for eng_name, aliases in RU_CLUBS.items():
        if eng_name.lower() == club_lower:
            return aliases[0].title()

    best_match = None
    best_match_len = 0
    for eng_name, aliases in RU_CLUBS.items():
        if len(eng_name) > 4 and eng_name.lower() in club_lower:
            if len(eng_name) > best_match_len:
                best_match = aliases[0].title()
                best_match_len = len(eng_name)

    if best_match:
        return best_match

    return club_en


def get_nation_ru_display(nation_en: str) -> str:
    aliases = RU_COUNTRIES.get(nation_en)
    if aliases:
        return aliases[0].title()
    return nation_en


def get_flag(country: str) -> str:
    return COUNTRY_FLAGS.get(country, "🏳️")


def get_position(pos: str) -> str:
    return POSITIONS_RU.get(pos, pos)


# --- ФУНКЦИИ РАБОТЫ С БАЗОЙ ДАННЫХ ---


def get_db_connection():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "football_bot.db")
    if not os.path.exists(db_path):
        return None
    return sqlite3.connect(db_path)


def generate_club_task():
    conn = get_db_connection()
    if not conn:
        return None
    cursor = conn.cursor()

    cursor.execute("""
        SELECT club_id, name, domestic_competition_id 
        FROM clubs 
        WHERE domestic_competition_id IN ('GB1', 'ES1', 'IT1', 'L1', 'FR1')
        ORDER BY RANDOM() LIMIT 1
    """)
    club_row = cursor.fetchone()
    if not club_row:
        return None

    club_id, club_name, league_id = club_row
    league_names = {
        "GB1": "АПЛ",
        "ES1": "Ла Лига",
        "IT1": "Серия А",
        "L1": "Бундеслига",
        "FR1": "Лига 1",
    }

    cursor.execute(
        """
        SELECT country_of_citizenship, position 
        FROM players WHERE current_club_id = ? 
        ORDER BY market_value_in_eur DESC LIMIT 11
    """,
        (club_id,),
    )

    hints = []
    for row in cursor.fetchall():
        nat = row[0] or "Unknown"
        pos = row[1] or "Unknown"

        ru_nat = get_nation_ru_display(nat)
        ru_pos = get_position(pos)

        hints.append(f"{get_flag(nat)} {ru_nat} — {ru_pos}")

    conn.close()
    random.shuffle(hints)

    return {
        "answer": club_name,
        "ru_answer": get_club_ru_display(club_name),
        "subtitle": league_names.get(league_id, league_id),
        "hints": hints,
    }


def generate_nation_task():
    conn = get_db_connection()
    if not conn:
        return None
    cursor = conn.cursor()

    nation = random.choice(list(RU_COUNTRIES.keys()))

    cursor.execute(
        """
        SELECT p.position, c.name 
        FROM players p
        JOIN clubs c ON p.current_club_id = c.club_id
        WHERE p.country_of_citizenship = ?
        ORDER BY p.market_value_in_eur DESC LIMIT 11
    """,
        (nation,),
    )

    hints = []
    for row in cursor.fetchall():
        pos = row[0] or "Unknown"
        club = row[1] or "Unknown"

        ru_pos = get_position(pos)
        ru_club = get_club_ru_display(club)

        hints.append(f"{ru_pos} — 🛡 {ru_club}")

    conn.close()
    random.shuffle(hints)

    ru_nation = get_nation_ru_display(nation)

    return {
        "answer": nation,
        "ru_answer": ru_nation,
        "subtitle": f"Сборная",
        "hints": hints,
    }


def generate_career_task():
    conn = get_db_connection()
    if not conn:
        return None
    cursor = conn.cursor()

    famous_players = list(RU_PLAYERS.keys())
    random.shuffle(famous_players)

    player_id = None
    player_name = None

    for name in famous_players:
        cursor.execute(
            "SELECT player_id, name FROM players WHERE name = ? LIMIT 1", (name,)
        )
        row = cursor.fetchone()
        if row:
            p_id, p_name = row
            cursor.execute(
                "SELECT COUNT(*) FROM transfers WHERE player_id = ?", (p_id,)
            )
            if cursor.fetchone()[0] > 0:
                player_id = p_id
                player_name = p_name
                break

    if not player_id:
        conn.close()
        return None

    cursor.execute(
        """
        SELECT transfer_season, from_club_name, to_club_name 
        FROM transfers 
        WHERE player_id = ? 
        ORDER BY transfer_date ASC
    """,
        (player_id,),
    )

    hints = []
    for row in cursor.fetchall():
        season, fr_club, to_club = row
        ru_fr_club = get_club_ru_display(fr_club)
        ru_to_club = get_club_ru_display(to_club)
        hints.append(f"📅 {season}: {ru_fr_club} ➡️ {ru_to_club}")

    conn.close()

    ru_display_name = RU_PLAYERS[player_name][0].title()

    return {
        "answer": player_name,
        "ru_answer": ru_display_name,
        "subtitle": "Футболист",
        "hints": hints,
    }


# --- ЛОГИКА БОТА ---

user_modes = {}
games = {}


class Game:
    def __init__(
        self, mode, player1_id, player1_name, player2_id=None, player2_name=None
    ):
        self.mode = mode
        self.player1_id = player1_id
        self.player1_name = player1_name
        self.player2_id = player2_id
        self.player2_name = player2_name
        self.is_solo = player2_id is None
        self.current_turn = player1_id

        self.score = {player1_id: 0}
        if not self.is_solo:
            self.score[player2_id] = 0
        self.losses = 0  # Для статистики в соло

        self.round = 1
        self.task = None
        self.revealed_count = 0
        self.attempts_after_all_hints = 0
        self.new_round()

    def new_round(self):
        if self.mode == "club":
            self.task = generate_club_task()
        elif self.mode == "nation":
            self.task = generate_nation_task()
        elif self.mode == "career":
            self.task = generate_career_task()

        self.revealed_count = 0
        self.attempts_after_all_hints = 0

    def get_current_hints_text(self):
        if not self.task or not self.task["hints"]:
            return "Ошибка генерации."

        shown = self.task["hints"][: self.revealed_count]
        lines = [
            f"📋 Подсказки ({self.revealed_count} из {len(self.task['hints'])}):",
            "",
        ]
        for i, hint in enumerate(shown, 1):
            lines.append(f"{i}. {hint}")
        return "\n".join(lines)

    def current_player_name(self):
        return (
            self.player1_name
            if self.current_turn == self.player1_id
            else self.player2_name
        )

    def switch_turn(self):
        if not self.is_solo:
            self.current_turn = (
                self.player2_id
                if self.current_turn == self.player1_id
                else self.player1_id
            )

    def reveal_one(self):
        if self.task and self.revealed_count < len(self.task["hints"]):
            self.revealed_count += 1

    def check_answer(self, guess: str) -> bool:
        guess_clean = guess.lower().strip()
        answer_en = self.task["answer"]
        answer_lower = answer_en.lower()

        if self.mode == "club":
            valid_answers = []
            for eng_name, aliases in RU_CLUBS.items():
                if eng_name.lower() == answer_lower or eng_name.lower() in answer_lower:
                    valid_answers.extend(aliases)

            if guess_clean in valid_answers or guess_clean in answer_lower:
                return True

        elif self.mode == "nation":
            valid_answers = RU_COUNTRIES.get(answer_en, [])
            if guess_clean in valid_answers or guess_clean in answer_lower:
                return True

        elif self.mode == "career":
            valid_answers = RU_PLAYERS.get(answer_en, [])
            last_name = answer_lower.split()[-1]
            if (
                guess_clean in valid_answers
                or guess_clean == answer_lower
                or guess_clean == last_name
            ):
                return True

        return False


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())


# Меню выбора игры
def mode_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🏙 Угадай клуб", callback_data="mode_club")],
            [
                InlineKeyboardButton(
                    text="🌍 Угадай сборную", callback_data="mode_nation"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🥾 Угадай игрока", callback_data="mode_career"
                )
            ],
        ]
    )


# Подменю (Соло / Кооп)
def type_keyboard(mode):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="👤 Соло", callback_data=f"type_solo_{mode}")],
            [
                InlineKeyboardButton(
                    text="👥 С другом (Кооп)", callback_data=f"type_coop_{mode}"
                )
            ],
            [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_modes")],
        ]
    )


def surrender_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🏳 Сдаться", callback_data="surrender")]
        ]
    )


@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "⚽ *Выбери режим игры:*",
        reply_markup=mode_keyboard(),
        parse_mode="Markdown",
    )


@dp.callback_query(F.data == "back_to_modes")
async def back_to_modes(callback: CallbackQuery):
    await callback.message.edit_text(
        "⚽ *Выбери режим игры:*", reply_markup=mode_keyboard(), parse_mode="Markdown"
    )


@dp.callback_query(F.data.startswith("mode_"))
async def select_mode(callback: CallbackQuery):
    mode = callback.data.split("_")[1]

    mode_names = {
        "club": "Угадай клуб",
        "nation": "Угадай сборную",
        "career": "Угадай игрока",
    }

    await callback.message.edit_text(
        f"✅ Выбран режим: *{mode_names[mode]}*\n\nКак будем играть?",
        reply_markup=type_keyboard(mode),
        parse_mode="Markdown",
    )


@dp.callback_query(F.data.startswith("type_"))
async def select_type(callback: CallbackQuery):
    parts = callback.data.split("_")
    game_type = parts[1]  # 'solo' или 'coop'
    mode = parts[2]
    chat_id = callback.message.chat.id

    user_modes[chat_id] = mode  # Сохраняем для /invite на случай если это кооп

    if game_type == "solo":
        game = Game(
            mode=mode,
            player1_id=callback.from_user.id,
            player1_name=callback.from_user.first_name,
        )
        if not game.task:
            await callback.answer("❌ Ошибка базы данных.", show_alert=True)
            return

        games[chat_id] = game
        game.reveal_one()

        await callback.message.delete()
        await bot.send_message(
            chat_id, "🔥 Соло-игра началась!\n\n⏳ Твой ход...", parse_mode="Markdown"
        )
        await asyncio.sleep(1)
        await send_turn(chat_id, game)

    elif game_type == "coop":
        games[chat_id] = {
            "pending": True,
            "host_id": callback.from_user.id,
            "host_name": callback.from_user.first_name,
            "mode": mode,
        }
        await callback.message.edit_text(
            f"👥 Выбран кооп-режим!\n\n"
            f"Напиши `/invite @username`, чтобы бросить вызов другу, "
            f"а он должен будет написать `/join`.",
            parse_mode="Markdown",
        )


@dp.message(Command("invite"))
async def cmd_invite(message: Message):
    chat_id = message.chat.id
    if chat_id not in user_modes:
        await message.answer("Сначала выбери режим игры через команду /start")
        return

    args = message.text.split()
    if len(args) < 2:
        await message.answer("Использование: /invite @username")
        return

    if chat_id in games and isinstance(games[chat_id], Game):
        await message.answer("Игра уже идёт! Сначала напиши /stop")
        return

    username = args[1].lstrip("@")

    # Перестраховка, если pending не был создан в кнопке
    if chat_id not in games or not isinstance(games[chat_id], dict):
        games[chat_id] = {
            "pending": True,
            "host_id": message.from_user.id,
            "host_name": message.from_user.first_name,
            "mode": user_modes[chat_id],
        }

    await message.answer(
        f"✅ Ждём @{username}!\n@{username}, напиши /join чтобы принять вызов."
    )


@dp.message(Command("join"))
async def cmd_join(message: Message):
    chat_id = message.chat.id
    pending = games.get(chat_id)

    if not pending or not isinstance(pending, dict) or not pending.get("pending"):
        await message.answer("Нет активного приглашения.")
        return

    if message.from_user.id == pending["host_id"]:
        await message.answer("Нельзя играть с самим собой.")
        return

    game = Game(
        mode=pending["mode"],
        player1_id=pending["host_id"],
        player1_name=pending["host_name"],
        player2_id=message.from_user.id,
        player2_name=message.from_user.first_name,
    )

    if not game.task:
        await message.answer("❌ Ошибка базы данных.")
        return

    games[chat_id] = game
    game.reveal_one()

    await message.answer(
        f"🔥 Игра началась!\n\n" f"⏳ Сейчас ход: {game.current_player_name()}..."
    )
    await asyncio.sleep(1)
    await send_turn(chat_id, game)


async def send_turn(chat_id: int, game: Game):
    text = (
        f"🏟 *{game.task['subtitle']}* | {game.task['ru_answer'] if game.revealed_count == len(game.task['hints']) else '...'}\n\n"
        f"{game.get_current_hints_text()}\n\n"
        f"Твой ответ 👇"
    )

    await bot.send_message(
        chat_id, text, reply_markup=surrender_keyboard(), parse_mode="Markdown"
    )


@dp.callback_query(F.data == "surrender")
async def handle_surrender(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    game = games.get(chat_id)

    if not game or isinstance(game, dict):
        await callback.answer("Игра не найдена")
        return

    if callback.from_user.id != game.current_turn:
        await callback.answer("Сейчас не твой ход!", show_alert=True)
        return

    await callback.answer()

    if game.is_solo:
        game.losses += 1
        await bot.send_message(
            chat_id,
            f"🏳 Ты сдался!\n\nОтвет: *{game.task['ru_answer']}* ({game.task['subtitle']})",
            parse_mode="Markdown",
        )
    else:
        game.switch_turn()
        winner_name = game.current_player_name()
        game.score[game.current_turn] += 1
        await bot.send_message(
            chat_id,
            f"🏳 {callback.from_user.first_name} сдался!\n\n"
            f"Ответ: *{game.task['ru_answer']}* ({game.task['subtitle']})\n\n"
            f"🎉 Очко получает {winner_name}!",
            parse_mode="Markdown",
        )

    game.round += 1
    if not game.is_solo:
        game.current_turn = game.player1_id if game.round % 2 == 1 else game.player2_id

    game.new_round()
    game.reveal_one()

    await asyncio.sleep(1.5)
    await show_scores_and_next(chat_id, game)


async def show_scores_and_next(chat_id: int, game: Game):
    if game.is_solo:
        wins = game.score[game.player1_id]
        await bot.send_message(
            chat_id,
            f"📊 Твой счет:\n✅ Угадано: {wins}\n❌ Не угадано: {game.losses}\n\n🔄 Следующий раунд!",
        )
    else:
        p1, p2 = game.player1_name, game.player2_name
        s1, s2 = game.score[game.player1_id], game.score[game.player2_id]
        await bot.send_message(
            chat_id, f"📊 Счёт: {p1} {s1} — {s2} {p2}\n\n🔄 Следующий раунд!"
        )

    await asyncio.sleep(1)
    await send_turn(chat_id, game)


@dp.message(Command("stop"))
async def cmd_stop(message: Message):
    chat_id = message.chat.id
    game = games.pop(chat_id, None)
    if not game:
        return await message.answer("Нет активной игры.")

    if isinstance(game, dict):
        return await message.answer("Ожидание отменено.")

    if game.is_solo:
        wins = game.score[game.player1_id]
        await message.answer(
            f"🛑 Игра остановлена.\n\nФинальный счёт:\n✅ Угадано: {wins}\n❌ Не угадано: {game.losses}",
            parse_mode="Markdown",
        )
    else:
        p1, p2 = game.player1_name, game.player2_name
        s1, s2 = game.score[game.player1_id], game.score[game.player2_id]
        winner = p1 if s1 > s2 else (p2 if s2 > s1 else None)
        result = f"🏆 Победитель: *{winner}*!" if winner else "🤝 Ничья!"

        await message.answer(
            f"🛑 Игра остановлена.\n\nФинальный счёт:\n{p1}: {s1}\n{p2}: {s2}\n\n{result}",
            parse_mode="Markdown",
        )


@dp.message()
async def handle_guess(message: Message):
    chat_id = message.chat.id
    game = games.get(chat_id)

    if not game or isinstance(game, dict) or message.from_user.id != game.current_turn:
        return

    guess = message.text.strip()

    if game.check_answer(guess):
        game.score[game.current_turn] += 1

        if game.is_solo:
            await message.answer(
                f"✅ *Правильно!*\n"
                f"Ответ: *{game.task['ru_answer']}* ({game.task['subtitle']}) 🎉",
                parse_mode="Markdown",
            )
        else:
            winner_name = game.current_player_name()
            await message.answer(
                f"✅ *{winner_name} угадал!*\n"
                f"Ответ: *{game.task['ru_answer']}* ({game.task['subtitle']}) 🎉",
                parse_mode="Markdown",
            )

        game.round += 1
        if not game.is_solo:
            game.current_turn = (
                game.player1_id if game.round % 2 == 1 else game.player2_id
            )

        game.new_round()
        game.reveal_one()

        await asyncio.sleep(1.5)
        await show_scores_and_next(chat_id, game)
    else:
        if game.revealed_count < len(game.task["hints"]):
            game.reveal_one()
            game.switch_turn()

            if game.is_solo:
                await message.answer(
                    "❌ Не то! Открываю следующую подсказку...", parse_mode="Markdown"
                )
            else:
                await message.answer(
                    f"❌ Не то!\nХод переходит к {game.current_player_name()}...",
                    parse_mode="Markdown",
                )

            await asyncio.sleep(0.8)
            await send_turn(chat_id, game)
        else:
            game.attempts_after_all_hints += 1
            game.switch_turn()

            max_attempts = 2 if game.is_solo else 4

            if game.attempts_after_all_hints >= max_attempts:
                if game.is_solo:
                    game.losses += 1
                    msg = f"❌ Попытки закончились!\nОтвет: *{game.task['ru_answer']}* ({game.task['subtitle']})\n\nПереходим к следующему раунду..."
                else:
                    msg = f"❌ Никто не угадал! Лимит попыток исчерпан.\nОтвет: *{game.task['ru_answer']}* ({game.task['subtitle']})\n\nПереходим к следующему раунду..."

                await message.answer(msg, parse_mode="Markdown")

                game.round += 1
                if not game.is_solo:
                    game.current_turn = (
                        game.player1_id if game.round % 2 == 1 else game.player2_id
                    )
                game.new_round()
                game.reveal_one()
                await asyncio.sleep(1.5)
                await show_scores_and_next(chat_id, game)
            else:
                attempts_left = max_attempts - game.attempts_after_all_hints
                if game.is_solo:
                    await message.answer(
                        f"❌ Не то!\n⚠️ Осталось попыток: *{attempts_left}*",
                        parse_mode="Markdown",
                    )
                else:
                    await message.answer(
                        f"❌ Не то!\nХод переходит к {game.current_player_name()}...\n⚠️ Осталось попыток на двоих: *{attempts_left}*",
                        parse_mode="Markdown",
                    )

                await asyncio.sleep(0.8)
                await send_turn(chat_id, game)


async def main():
    print("🤖 Бот запущен (Режимы: Соло и Кооп)")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
