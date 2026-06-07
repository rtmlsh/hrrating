from datetime import date


UPDATED_AT = date(2026, 6, 1)

# Производственный календарь РФ 2026
MONTHS_2026 = [
    {"value": 1,  "label": "Январь 2026",   "working_days": 15},
    {"value": 2,  "label": "Февраль 2026",  "working_days": 19},
    {"value": 3,  "label": "Март 2026",     "working_days": 21},
    {"value": 4,  "label": "Апрель 2026",   "working_days": 22},
    {"value": 5,  "label": "Май 2026",      "working_days": 18},
    {"value": 6,  "label": "Июнь 2026",     "working_days": 21},
    {"value": 7,  "label": "Июль 2026",     "working_days": 23},
    {"value": 8,  "label": "Август 2026",   "working_days": 21},
    {"value": 9,  "label": "Сентябрь 2026", "working_days": 22},
    {"value": 10, "label": "Октябрь 2026",  "working_days": 22},
    {"value": 11, "label": "Ноябрь 2026",   "working_days": 20},
    {"value": 12, "label": "Декабрь 2026",  "working_days": 23},
]

# Прогрессивная шкала НДФЛ 2026
NDFL_RATES = [
    {"value": 13, "label": "13% — до 2 400 000 ₽/год",        "threshold": "до 200 000 ₽/мес"},
    {"value": 15, "label": "15% — до 5 000 000 ₽/год",        "threshold": "до 417 000 ₽/мес"},
    {"value": 18, "label": "18% — до 20 000 000 ₽/год",       "threshold": "до 1 667 000 ₽/мес"},
    {"value": 20, "label": "20% — до 50 000 000 ₽/год",       "threshold": "до 4 167 000 ₽/мес"},
    {"value": 22, "label": "22% — свыше 50 000 000 ₽/год",    "threshold": "свыше 4 167 000 ₽/мес"},
]

LEVELS = [
    {"key": "junior", "label": "Junior", "multiplier": 0.66, "spread": 0.22},
    {"key": "middle", "label": "Middle", "multiplier": 1.0, "spread": 0.20},
    {"key": "senior", "label": "Senior", "multiplier": 1.58, "spread": 0.22},
    {"key": "lead", "label": "Lead", "multiplier": 2.08, "spread": 0.24},
]

INDUSTRIES = [
    {"key": "hr", "label": "HR и рекрутинг", "multiplier": 1.0},
    {"key": "it", "label": "IT", "multiplier": 1.18},
    {"key": "finance", "label": "Финансы", "multiplier": 1.12},
    {"key": "retail", "label": "Ритейл", "multiplier": 0.92},
    {"key": "production", "label": "Производство", "multiplier": 0.98},
    {"key": "pharma", "label": "Фарма", "multiplier": 1.10},
    {"key": "logistics", "label": "Логистика", "multiplier": 0.95},
]

CITIES = [
    {"key": "moscow", "label": "Москва", "multiplier": 1.0},
    {"key": "spb", "label": "Санкт-Петербург", "multiplier": 0.84},
    {"key": "regions", "label": "Регионы", "multiplier": 0.64},
]

PROFESSIONS = [
    {"name": "HR-менеджер", "middle": 120000, "growth": 1.14},
    {"name": "Рекрутер", "middle": 105000, "growth": 1.12},
    {"name": "IT-рекрутер", "middle": 155000, "growth": 1.18},
    {"name": "HR-директор", "middle": 235000, "growth": 1.10},
    {"name": "HR Business Partner", "middle": 165000, "growth": 1.16},
    {"name": "HR Generalist", "middle": 130000, "growth": 1.12},
    {"name": "People Partner", "middle": 175000, "growth": 1.17},
    {"name": "Talent Acquisition Manager", "middle": 155000, "growth": 1.14},
    {"name": "Talent Sourcer", "middle": 110000, "growth": 1.13},
    {"name": "Массовый рекрутер", "middle": 92000, "growth": 1.08},
    {"name": "Executive Search консультант", "middle": 205000, "growth": 1.15},
    {"name": "Специалист по КДП", "middle": 102000, "growth": 1.07},
    {"name": "Инспектор по кадрам", "middle": 92000, "growth": 1.06},
    {"name": "C&B специалист", "middle": 150000, "growth": 1.13},
    {"name": "Payroll specialist", "middle": 118000, "growth": 1.08},
    {"name": "HR-аналитик", "middle": 165000, "growth": 1.19},
    {"name": "HR Ops manager", "middle": 155000, "growth": 1.13},
    {"name": "L&D менеджер", "middle": 138000, "growth": 1.12},
    {"name": "Менеджер по обучению", "middle": 132000, "growth": 1.11},
    {"name": "T&D специалист", "middle": 125000, "growth": 1.10},
    {"name": "Специалист по адаптации", "middle": 108000, "growth": 1.09},
    {"name": "Employer Brand Manager", "middle": 145000, "growth": 1.15},
    {"name": "Специалист по внутренним коммуникациям", "middle": 128000, "growth": 1.11},
    {"name": "HR marketing manager", "middle": 142000, "growth": 1.14},
    {"name": "Руководитель отдела персонала", "middle": 200000, "growth": 1.10},
    {"name": "Директор по персоналу", "middle": 245000, "growth": 1.10},
    {"name": "Head of Talent Acquisition", "middle": 230000, "growth": 1.14},
    {"name": "Head of C&B", "middle": 245000, "growth": 1.12},
    {"name": "HR project manager", "middle": 150000, "growth": 1.15},
    {"name": "HR product manager", "middle": 185000, "growth": 1.18},
    {"name": "People Analytics Lead", "middle": 220000, "growth": 1.20},
    {"name": "HRIS manager", "middle": 165000, "growth": 1.16},
    {"name": "Специалист по оценке персонала", "middle": 132000, "growth": 1.10},
    {"name": "Assessment manager", "middle": 150000, "growth": 1.11},
    {"name": "Специалист по мотивации", "middle": 135000, "growth": 1.11},
    {"name": "Compensation analyst", "middle": 155000, "growth": 1.13},
    {"name": "HR compliance specialist", "middle": 128000, "growth": 1.09},
    {"name": "Специалист по охране труда", "middle": 112000, "growth": 1.08},
    {"name": "Ресечер", "middle": 85000, "growth": 1.11},
    {"name": "Рекрутер массового подбора", "middle": 90000, "growth": 1.08},
    {"name": "Рекрутер в ритейле", "middle": 95000, "growth": 1.08},
    {"name": "Рекрутер в производстве", "middle": 105000, "growth": 1.09},
    {"name": "Финансовый рекрутер", "middle": 145000, "growth": 1.12},
    {"name": "Tech sourcer", "middle": 130000, "growth": 1.17},
    {"name": "Global mobility specialist", "middle": 140000, "growth": 1.10},
    {"name": "Relocation manager", "middle": 120000, "growth": 1.09},
    {"name": "Culture manager", "middle": 130000, "growth": 1.11},
    {"name": "Diversity & Inclusion manager", "middle": 145000, "growth": 1.13},
    {"name": "Office manager", "middle": 85000, "growth": 1.06},
    {"name": "Административный директор", "middle": 165000, "growth": 1.08},
    {"name": "Бизнес-ассистент", "middle": 115000, "growth": 1.09},
    {"name": "Корпоративный психолог", "middle": 125000, "growth": 1.10},
    {"name": "Специалист по wellbeing", "middle": 118000, "growth": 1.12},
    {"name": "Менеджер кадрового агентства", "middle": 135000, "growth": 1.11},
    {"name": "Аккаунт-менеджер HR-агентства", "middle": 125000, "growth": 1.10},
]

TOP_TABLE = [
    ("HR-менеджер", "60-80 тыс.", "100-140 тыс.", "180-250 тыс.", "240-320 тыс."),
    ("Рекрутер", "55-75 тыс.", "90-120 тыс.", "150-200 тыс.", "190-260 тыс."),
    ("IT-рекрутер", "70-100 тыс.", "130-180 тыс.", "200-300 тыс.", "280-400 тыс."),
    ("HR-директор", "-", "180-250 тыс.", "300-500 тыс.", "450-650 тыс."),
    ("HR Business Partner", "90-120 тыс.", "140-190 тыс.", "220-320 тыс.", "320-450 тыс."),
    ("HR Generalist", "65-85 тыс.", "110-150 тыс.", "170-230 тыс.", "220-300 тыс."),
    ("People Partner", "90-120 тыс.", "140-200 тыс.", "220-330 тыс.", "300-430 тыс."),
    ("Talent Acquisition Manager", "75-105 тыс.", "130-180 тыс.", "200-290 тыс.", "280-390 тыс."),
    ("Talent Sourcer", "55-80 тыс.", "90-130 тыс.", "140-200 тыс.", "180-250 тыс."),
    ("Массовый рекрутер", "50-70 тыс.", "80-110 тыс.", "120-160 тыс.", "150-210 тыс."),
    ("Executive Search консультант", "90-130 тыс.", "160-240 тыс.", "280-450 тыс.", "400-700 тыс."),
    ("Специалист по КДП", "55-75 тыс.", "85-120 тыс.", "130-180 тыс.", "170-230 тыс."),
    ("C&B специалист", "75-100 тыс.", "130-180 тыс.", "200-300 тыс.", "300-420 тыс."),
    ("L&D менеджер", "70-95 тыс.", "120-170 тыс.", "180-260 тыс.", "250-360 тыс."),
    ("HR-аналитик", "80-110 тыс.", "140-190 тыс.", "220-320 тыс.", "300-420 тыс."),
    ("HR Ops manager", "75-105 тыс.", "130-180 тыс.", "200-280 тыс.", "260-380 тыс."),
    ("Employer Brand Manager", "70-100 тыс.", "120-170 тыс.", "180-250 тыс.", "250-350 тыс."),
    ("Специалист по адаптации", "55-75 тыс.", "90-125 тыс.", "130-180 тыс.", "170-230 тыс."),
    ("Менеджер по обучению", "65-90 тыс.", "110-160 тыс.", "170-240 тыс.", "230-320 тыс."),
    ("Специалист по внутренним коммуникациям", "65-90 тыс.", "110-155 тыс.", "160-230 тыс.", "220-310 тыс."),
]

FAQ_ITEMS = [
    (
        "Какая средняя зарплата HR-менеджера в Москве в 2026 году?",
        "В базе HR Rating для Москвы медианная зарплата HR-менеджера уровня Middle составляет 120 000 руб. в месяц, типичная вилка - 95 000-145 000 руб. Для Senior-уровня ориентир выше: около 190 000 руб. медианы и до 250 000 руб. в верхней части вилки.",
    ),
    (
        "Сколько зарабатывает рекрутер без опыта?",
        "Junior-рекрутер без опыта или с опытом до года в Москве обычно попадает в диапазон 55 000-75 000 руб. в месяц. В IT, финансах и executive search старт может быть выше, но работодатели чаще ждут навыки сорсинга, работы с воронкой и самостоятельного ведения вакансий.",
    ),
    (
        "Как рассчитать достойную зарплату для своей профессии?",
        "Сравните медиану по профессии, уровень опыта, отрасль и город. Затем проверьте, какие задачи входят в роль: самостоятельное закрытие вакансий, аналитика, управление командой, бюджетирование и HR-стратегия обычно повышают вилку сильнее, чем формальный стаж.",
    ),
    (
        "Влияет ли размер компании на зарплату HR?",
        "Да. В малом бизнесе HR-специалист часто совмещает подбор, КДП и адаптацию, поэтому зарплата ближе к нижней части вилки. В средних и крупных компаниях роли разделены, появляются C&B, HRBP, People Analytics и HR Ops, а компенсация чаще включает бонусы за проекты и закрытие вакансий.",
    ),
    (
        "Какие надбавки и бонусы типичны для HR-специалистов?",
        "Для рекрутеров распространены бонусы за закрытые вакансии и качество выхода кандидатов. Для HRBP, C&B и руководителей чаще встречаются квартальные или годовые премии, бонусы за удержание персонала, выполнение HR-проектов и достижение бизнес-показателей подразделения.",
    ),
    (
        "Как зарплаты в Москве отличаются от регионов?",
        "Москва обычно является верхней точкой рынка. Санкт-Петербург в среднем на 15-20% ниже московской вилки, регионы - на 30-40% ниже, но удалённые IT-команды и федеральные работодатели могут платить ближе к московскому уровню.",
    ),
    (
        "Чем отличается оклад HR BP от generalist HR?",
        "HR Generalist закрывает широкий операционный контур: подбор, адаптацию, КДП, коммуникации и базовую аналитику. HR Business Partner работает ближе к бизнес-юнитам, влияет на оргструктуру, удержание, мотивацию и performance-процессы, поэтому медианная вилка HRBP обычно выше.",
    ),
    (
        "Когда лучше просить повышение зарплаты?",
        "Лучший момент - после измеримого результата: закрытия сложных вакансий, снижения текучести, запуска системы адаптации, автоматизации HR-процесса или успешного пересмотра грейдов. Подготовьте рыночную вилку, список достижений и вариант новой зоны ответственности.",
    ),
]

SOURCE_LINKS = [
    {
        "label": "hh.ru: вакансии и карьерные материалы",
        "url": "https://hh.ru/search/vacancy?area=1&text=HR-%D0%BC%D0%B5%D0%BD%D0%B5%D0%B4%D0%B6%D0%B5%D1%80",
    },
    {
        "label": "SuperJob: статистика зарплат по HR-ролям",
        "url": "https://www.superjob.ru/zarplata/",
    },
    {
        "label": "Росстат: рынок труда, занятость и заработная плата",
        "url": "https://rosstat.gov.ru/labor_market_employment_salaries",
    },
]


def _lookup(items, key, default_key):
    return next((item for item in items if item["key"] == key), next(item for item in items if item["key"] == default_key))


def _round_salary(value):
    return int(round(value / 5000) * 5000)


def _format_money(value):
    return f"{value:,.0f}".replace(",", " ")


def _format_range(min_salary, max_salary):
    return f"{min_salary // 1000}-{max_salary // 1000} тыс. руб."


def find_profession(name):
    normalized = (name or "").strip().lower()
    if not normalized:
        return PROFESSIONS[0]
    exact = next((item for item in PROFESSIONS if item["name"].lower() == normalized), None)
    if exact:
        return exact
    contains = next((item for item in PROFESSIONS if normalized in item["name"].lower()), None)
    return contains or PROFESSIONS[0]


def calculate_salary(profession_name="HR-менеджер", level_key="middle", industry_key="hr", city_key="moscow"):
    profession = find_profession(profession_name)
    level = _lookup(LEVELS, level_key, "middle")
    industry = _lookup(INDUSTRIES, industry_key, "hr")
    city = _lookup(CITIES, city_key, "moscow")

    median_salary = _round_salary(profession["middle"] * level["multiplier"] * industry["multiplier"] * city["multiplier"])
    min_salary = _round_salary(median_salary * (1 - level["spread"]))
    max_salary = _round_salary(median_salary * (1 + level["spread"]))
    market_median = _market_median(level, industry, city)
    delta = round((median_salary - market_median) / market_median * 100)

    if delta >= 8:
        comparison = f"на {delta}% выше среднего по выборке"
        comparison_tone = "high"
    elif delta <= -8:
        comparison = f"на {abs(delta)}% ниже среднего по выборке"
        comparison_tone = "low"
    else:
        comparison = "около среднего уровня рынка"
        comparison_tone = "average"

    return {
        "profession": profession["name"],
        "level": level["key"],
        "level_label": level["label"],
        "industry": industry["key"],
        "industry_label": industry["label"],
        "city": city["key"],
        "city_label": city["label"],
        "median": median_salary,
        "median_display": f"{_format_money(median_salary)} руб.",
        "min": min_salary,
        "max": max_salary,
        "range_display": _format_range(min_salary, max_salary),
        "comparison": comparison,
        "comparison_tone": comparison_tone,
        "updated_at": UPDATED_AT.isoformat(),
        "updated_label": UPDATED_AT.strftime("%d.%m.%Y"),
    }


def _market_median(level, industry, city):
    values = [
        _round_salary(item["middle"] * level["multiplier"] * industry["multiplier"] * city["multiplier"])
        for item in PROFESSIONS
    ]
    midpoint = len(values) // 2
    ordered = sorted(values)
    return ordered[midpoint]


def build_payload(selection=None):
    selection = selection or {}
    profession = selection.get("profession", "HR-менеджер")
    level = selection.get("level", "middle")
    industry = selection.get("industry", "hr")
    city = selection.get("city", "moscow")
    result = calculate_salary(profession, level, industry, city)

    return {
        "updated_at": UPDATED_AT.isoformat(),
        "updated_label": UPDATED_AT.strftime("%d.%m.%Y"),
        "professions": PROFESSIONS,
        "levels": LEVELS,
        "industries": INDUSTRIES,
        "cities": CITIES,
        "selection": {
            "profession": result["profession"],
            "level": result["level"],
            "industry": result["industry"],
            "city": result["city"],
        },
        "result": result,
        "charts": build_chart_data(result["profession"], industry, city),
    }


def build_chart_data(profession_name, industry_key="hr", city_key="moscow"):
    profession = find_profession(profession_name)
    industry = _lookup(INDUSTRIES, industry_key, "hr")
    city = _lookup(CITIES, city_key, "moscow")

    by_level = [
        {
            "label": level["label"],
            "value": _round_salary(profession["middle"] * level["multiplier"] * industry["multiplier"] * city["multiplier"]),
        }
        for level in LEVELS
    ]
    middle_now = _round_salary(profession["middle"] * industry["multiplier"] * city["multiplier"])
    trend = [
        {"label": "2024", "value": _round_salary(middle_now / profession["growth"] / 1.07)},
        {"label": "2025", "value": _round_salary(middle_now / profession["growth"])},
        {"label": "2026", "value": middle_now},
    ]
    by_industry = [
        {
            "label": item["label"],
            "value": _round_salary(profession["middle"] * item["multiplier"] * city["multiplier"]),
        }
        for item in INDUSTRIES
    ]
    return {
        "profession": profession["name"],
        "by_level": by_level,
        "trend": trend,
        "by_industry": by_industry,
    }


def top_table_rows():
    return [
        {"profession": row[0], "junior": row[1], "middle": row[2], "senior": row[3], "lead": row[4]}
        for row in TOP_TABLE
    ]
