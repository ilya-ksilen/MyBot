import logging
logging.basicConfig(
    level = logging.INFO, 
    format = '%(asictime)s - %(levelname)s - %(message)s'
)
import random

#маски всех инструментов
MASK = {
"kick1":[1,0,0,0],
    "snare1": [0,0,0,0,1,0,0,0],
    "snare2": [0,0,0,1,0,0,0,1],
    "snare3":[0,0,0,1,0,0,0,0],
    "snare4":[0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0],
    "ch1":[1,1,1,1],
    "ch2":[0,1,1,0],
    "ch3":[0,0,1,0],
    "ch4":[1,0,1,0],
    "ch5":[0,1,0,1],
    "ch6":[0,0,1,1],
    "oh1":[0,0,1,0],
    "oh2":[1,0,0,0],
    "shaker1":[0,1,0,1,0,0,1,0,0,1,0,1,0,0,1,0],
    "shaker2":[1,0,1,1,0,0,0,0],
    "shaker3":[0,1,1,0],
    "clap1":[0,0,0,1],
    "clap2":[0,0,0,1,0,0,0,0],
    "clap3":[0,0,0,0,0,0,0,1],
    "tom1":[0,0,1,0,0,1,0,0,0,0,1,0,0,1,0,0],
    "tom2":[1,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0],
    "tom3":[1,1,0,1],
    "cong1":[0,0,1,0,1,0,0,0,0,0,1,0,1,0,0,0],
    "cong2":[1,0,1,1],
    "cong3":[0,0,0,0,1,0,1,0],
    "bong1":[1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0],
    "bong2":[1,0,0,0,0,0,1,0],
    "bong3":[1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,],
    "rimshot1":[0,0,0,0,1,0,0,0],
    "rimshot2":[1,0,0,0,1,0,0,0],
    "ride1":[1,0,0,0],
    "ride2":[1,0,1,0],
    "crash1":[0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],
    "crash2":[1,0,0,0,0,0,0,0],
    "crash3":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
    "bell1":[0,0,1,0],
    "bell2":[0,0,1,1],
    "bell3":[1,0,0,0],
    "bell4":[0,1],
    #"industrial1":[],
    #"glitch1":[]
}

def get_mask (name):
    if name in MASK:
        return MASK[name]
    else:
        logging.warning(f"Маска {name} не найдена! Пропускаю")
        return None

#связь инстуремнтов с их масками
PATTERN_INST = {
    "kick":["kick1"],
    "snare":["snare1","snare2","snare3","snare4"],
    "closehat":["ch1","ch2","ch3","ch4","ch5","ch6"],
    "openhat":["oh1","oh2"],
    "clap":["clap1","clap2","clap3"],
    "rimshot":["rimshot1","rimshot2"],
    "ride":["ride1","ride2"],
    "crash":["crash1","crash2","crash3"],
    "shaker":["shaker1","shaker2","shaker3"],
    "cong":["cong1","cong2","cong3"],
    "bong":["bong1","bong2","bong3"],
    "tom":["tom1","tom2","tom3"],
    "bell":["bell1","bell2","bell3","bell4"],
    #"indastrial":["industrial1"],
    #"glitch":["glitch1"]
}
def select_instruments():
    all_instruments = list(PATTERN_INST.keys())
    others = [inst for inst in all_instruments if inst not in ["kick","snare"]]
    count_others = random.randint(4,6)
    selected_others = random.sample(others,min(count_others,len(others))) #безопасность кода (чтобы не взял больше)
    return ["kick","snare"] + selected_others

def generate_loop (instruments, steps=16):
    result = {}
    for instrument in instruments:
        patterns = PATTERN_INST [instrument]
        chosen = random.choice(patterns)
        mask = get_mask(chosen)
        full = []
        for i in range(steps):
            full.append(mask[i%len(mask)])
            result[instrument]=full
     return result

def generate_random_loop(steps=16):
    instruments = select_instruments()
    loop = generate_loop(instruments,steps=16)
    return loop

    

#визуальная часть
def visualize_loop (loop):
    header = "      " + " ".join(f"{i:2d}" for i in range(16))
    lines = [header]
    for inst in PATTERN_INST.keys():
        if inst in loop:
            pattern = loop [inst]
        else:
            pattern = [0] * 16
        row = f"{inst:6s}"
        for val in pattern:
            if val == 1:
                row += "🟥"
            else:
                row += "⬛"
        lines.append(row)
    return "\n".join(lines)


