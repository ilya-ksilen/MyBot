import logging
logging.basicConfig(level=logging.INFO,format="%(asctime)s - %(levelname)s - %(message)s")

Masks_bass = {
    "simple":[1,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0],
    "offbeat": [0,0,1,0],
    "live11": [1,0,0,1,0,0,1,0,0,1,0],
    "live12":[1,0,0,1,0,0,1,0,0,1,0,0],
    "live13":[1,0,0,1,0,0,1,0,0,1,0,0,0],
    "live16":[1,0,0,1,0,0,1,0,0,1,0,0,0,0,0,0]
}
def get_mask_b (name):
    if name in Masks_bass:
        return Masks_bass [name]
    else:
        logging.warning(f"Маска: {name} не найдена! Использую по умолчанию simple.")
        return Masks_bass["simpe"]

Masks_lead = {
    "rand1":[1,1,1,0,0,0,0,0,1,1,1,1,0,0,1,1],
    "rand2":[1,1,0,0,1,0,1,0],
    "rand3":[0,0,1,0,0,1,0,1],
    "rand4":[1,1,0,0],
    "rand5":[1,1,1,0,0,0,0,0,0,1,1,1,0,0,0,0]
}
def get_mask_l (name):
    if name in Masks_lead:
        return Masks_lead [name]
    else:
        logging.warning(f"Маска {name} не найдена! Использую по умолчанию rand1.") 
        return Masks_lead ["rand4"]

Scale_key = {
    "minor": [0,2,3,5,7,8,10],
    "major":[0,2,4,5,7,9,11],
    "dor":[0,2,3,5,7,9,10],
    "frig":[0,1,3,5,7,8,10]
}
def get_key (name):
    if name in Scale_key:
        return Scale_key ["minor"]
    else:
        logging.warning(f"Scale: {name} не найден! Использую по умолчанию minor.")
        return Scale_key ["minor"]    

def generate_bass (config):
    root_note = config["root_note"]
    scale = Scale_key(config["scale"])
    mask = get_mask_b(config["mask"])
    steps = config["steps"]
    oct_shift = config["oct_shift"]

    count_note = 0
    result=[]
    for i in range(steps):
        note_idx = i%len(root_note)
        scale_idx = i%len(scale)
        mask_idx = i%len(mask)

        note = root_note[note_idx] + scale[scale_idx] + oct_shift

        if mask[mask_idx] = 1:
            result.append(note)
            count_note +=1
        else:
            result-append(None)
    return result,count_note

def generate_lead (config):
    root_note = config["root_note"]
    scale = Scale_key(config["scale"])
    mask = Masks_leaad(config["mask"])
    steps = config["steps"]
    oct_shift = config["oct_shift"]

    result=[]
    count_note=0
    for i in range(steps):
        note_idx = i%len(root_note)
        scale_idx = i%len(scale)
        mask_idx = i%len(mask)

        note = root_note[note_idx] + scale[scale_idx] + oct_shift
        if mask = 1:
            result.append(note)
            count_note =+1
        else:
            result.append(None)
    return result


#далее прописать конфиги для бас линии и для лид линии
