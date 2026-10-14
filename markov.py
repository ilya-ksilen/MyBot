# Задача: написать логику заполнения паттерна
# Первое это плотность заполнения паттерна.
# Для начала на каждом шаге разыгрывается будет ли нота, НО при этом плотность должна быть равномерной по паттерну
# Чтобы не получилось, что к примеру 45% плотность ляжет на первую половину паттерна, а дальше пусто.
# Далее разыгрыввается какая нота (скорее всего тонику берем из лада)
# Далее заполненная нота остается обязательно в памяти
# Далее разыгрывается какая нота, отталкиваясь от того какая предыдущая была 
# И здесь же учитывается как давно нота была
# Здесь же учитывается как далеко эта нота (муз интервалы)
# Далее разыгрывается, учитывая всю предыдущую инфу направление куда пойдет нота (тоже вероятности просчитаны на это)
# НО если вся дистанция паттерна уже становится длинне, чем допустимо, то точно разворачивается направление.

#ВЫДЕРЖКА:
# Логика генерации на основе цепей Маркова
# Цепь: Лад - плотность - интервал - направление - снэп на ноту в ладу - проверка ограничений

import random

SCALES = {
    "major":[0,2,4,5,7,9,11],
    "minor": [0,2,3,5,7,8,10],
    "dor":[0,2,3,5,7,9,10],
    "frig":[0,1,3,5,7,8,10],
    "atonal":None
}

SCALE_PROBS = {
    "detroit_bass":{"major": 0.075,"minor": 0.375,"dor": 0.225,"frig": 0.325},
    "detroit_lead":{"major": 0.075,"minor": 0.325,"dor": 0.375,"frig": 0.225},
    "industrial_bass":{"major": 0.025,"minor": 0.375,"dor": 0.125,"frig": 0.475},
    "industrial_lead":{"major": 0.025,"minor": 0.225,"dor": 0.125,"frig": 0.350,"atonal": 0.275}
}

MAX_DIST = {
    "detroit_bass": 7,
    "detroit_lead": 10,
    "industrial_bass": 9,
    "industrial_lead": 9
}

DENSITY = {
    "detroit_bass": [0.90, 0.35, 0.65, 0.40, 0.55, 0.30, 0.65, 0.45, 0.80, 0.35, 0.65, 0.40, 0.55, 0.30, 0.70, 0.35],
    "detroit_lead": [0.75, 0.20, 0.40, 0.25, 0.50, 0.30, 0.45, 0.35, 0.65, 0.25, 0.45, 0.30, 0.55, 0.20, 0.50, 0.25],
    "industrial_bass": [0.70, 0.55, 0.65, 0.50, 0.60, 0.45, 0.65, 0.55, 0.75, 0.55, 0.65, 0.50, 0.65, 0.45, 0.70, 0.50],
    "industrial_lead": [0.50, 0.15, 0.25, 0.15, 0.35, 0.20, 0.30, 0.20, 0.45, 0.10, 0.20, 0.15, 0.35, 0.10, 0.25, 0.15]
}
INTERVAL_PROBS = {
    "detroit_bass": [
        (0,  0.30, 0.15, 0.20), 
        (1,  0.075,0.20, 0.175),
        (2,  0.075,0.20, 0.175),
        (3,  0.10, 0.125,0.125),
        (4,  0.10, 0.125,0.125),
        (5,  0.10, 0.05, 0.05),
        (7,  0.10, 0.05, 0.05),
        (12, 0.15, 0.10, 0.10),
    ],
    "detroit_lead": [
        (0,  0.15, 0.15, 0.20),
        (1,  0.075,0.10, 0.075),
        (2,  0.075,0.10, 0.075),
        (3,  0.125,0.125,0.10),
        (4,  0.125,0.125,0.10),
        (5,  0.125,0.10, 0.10),
        (7,  0.125,0.10, 0.10),
        (12, 0.20, 0.20, 0.25),
    ],
    "industrial_bass": [
        (0,  0.10, 0.10, 0.15),
        (1,  0.10, 0.125,0.125),
        (2,  0.10, 0.125,0.125),
        (3,  0.075,0.075,0.075),
        (4,  0.075,0.075,0.075),
        (5,  0.10, 0.075,0.075),
        (6,  0.10, 0.10, 0.05),
        (7,  0.10, 0.075,0.075),
        (12, 0.25, 0.25, 0.25),
    ],
    "industrial_lead": [
        (0,  0.45, 0.45, 0.50),
        (1,  0.05, 0.075,0.05),
        (2,  0.05, 0.075,0.05),
        (3,  0.05, 0.05, 0.05),
        (4,  0.05, 0.05, 0.05),
        (5,  0.075,0.05, 0.05),
        (6,  0.05, 0.05, 0.05),
        (7,  0.075,0.05, 0.05),
        (12, 0.15, 0.15, 0.15),
    ]
}

UP_PROBS = {
    "detroit_bass": {"strong": 0.40, "weak": 0.55, "even": 0.50},
    "detroit_lead": {"strong": 0.50, "weak": 0.55, "even": 0.50},
    "industrial_bass": {"strong": 0.45, "weak": 0.55, "even": 0.50},
    "industrial_lead": {"strong": 0.50, "weak": 0.50, "even": 0.50}
}

def weighted_choice(weights):
    if isinstance(weights, dict):
        items = list(weights.items())
    else:
        items = list(weights)
    total = sum(prob for _, prob in items)
    r = random.random() * total
    acc = 0.0
    for value, prob in items:
        acc += prob
        if acc >= r:
            return value
    return items [-1][0]    


def step_bucket(step):
    if step in (1, 5, 9, 13):
        return "strong"
    elif step in (3, 7, 11, 15):
        return "weak"
    else:
        return "even"


def snap_to_scale(note,scale):
    if scale is None:
        return note
    octave = note //12
    pitch = note % 12
    candidates = []
    for n in scale:
        candidates.append(n)
        candidates.append(n+12)
        candidates.append(n-12)
    best = min(candidates, key=lambda c: (abs(c - pitch),c))
    return octave * 12 + best 

def start_note(scale):
    start = weighted_choice({0:0.80, 2:0.15, 4:0.05}) #вероятности тоники первой нотой
    return scale[start]

def select_interval(intervals, bucket):
    bucket_idx = {"strong": 0, "weak": 1, "even": 2}[bucket]
    weights = [(iv, probs[bucket_idx]) for iv, *probs in intervals]
    return weighted_choice(weights)

# def generate_bar()
# def generate_markov()


if __name__ == "__main__":
    # print(step_bucket(1))
    # print(step_bucket(2))
    # print(step_bucket(3))
    # print(step_bucket(5))
    # print(step_bucket(15))
    # print(step_bucket(16))
    # minor = [0,2,3,5,7,8,10]
    # print(snap_to_scale(15, minor))
    # print(snap_to_scale(6, minor))
    # print(snap_to_scale(24, minor))
    # print(snap_to_scale(4, None))
    detroit = [
        (0,  0.30, 0.15, 0.20), 
        (1,  0.075,0.20, 0.175),
        (2,  0.075,0.20, 0.175),
        (3,  0.10, 0.125,0.125),
        (4,  0.10, 0.125,0.125),
        (5,  0.10, 0.05, 0.05),
        (7,  0.10, 0.05, 0.05),
        (12, 0.15, 0.10, 0.10),
    ]
    for _ in range(100):
        print(select_interval(detroit, "strong"))
    for _ in range(100):
        print(select_interval(detroit, "weak"))
    for _ in range(100):
        print(select_interval(detroit, "even"))


