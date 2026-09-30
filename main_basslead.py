from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import random
import logging
logging.basicConfig(level=logging.INFO,format="%(asctime)s - %(levelname)s - %(message)s")

Masks_bass = {
    "simple":[1,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0],
    "offbeat": [0,0,1,0],
    "swing": [1,0,0,1,0,1,0,0,1,0,1,0],
    "power":[1,1,0,1,1,1,0,1,1,1,0,1,1,0,1,0],
    "voltage":[1,0,1,0,1,1,0,1,0,1,0,1,0,0,0,0], #название можно поменять
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
        return Masks_bass["simple"]

# Связь режима с масками
PATTERN_BASS = ["simple","offbeat","swing","power","voltage","live11","live12","live13","live16"]
PATTERN_LEAD = ["rand1","rand2","rand3","rand4","rand5"]

# словари режимов и поч настр
NOTES = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
SCALES = ["minor","major","frig","dor"]
GENRES = ["detroit","industrial"]
GENRE_EMOJI = {
    "detroit": "☺",
    "industrial": "🏭"
}
MODES = ["bass","lead"]
MODES_EMOJI = {
    "bass": '🎸',
    "lead": '🎹'
}
STEPS = [16,32,64]

LAYOUT = {
    16:(8,2),
    32:(16,2),
    64:(16,4)
}

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
        return Masks_lead ["rand1"]

Scale_key = {
    "minor": [0,2,3,5,7,8,10],
    "major":[0,2,4,5,7,9,11],
    "dor":[0,2,3,5,7,9,10],
    "frig":[0,1,3,5,7,8,10]
}
def get_key (name):
    if name in Scale_key:
        return Scale_key[name]
    else:
        logging.warning(f"Scale: {name} не найден! Использую по умолчанию minor.")
        return Scale_key ["minor"]    


def generate_bass (config):
    root_note = config["root_note"]
    scale = get_key(config["scale"])
    mask = get_mask_b(config["mask"])
    steps = config["steps"]
    oct_shift = config["oct_shift"]

    count_note = 0
    result=[]
    for i in range(steps):
        scale_idx = i%len(scale)
        mask_idx = i%len(mask)

        note = root_note + scale[scale_idx] + oct_shift

        if mask[mask_idx] == 1:
            result.append(note)
            count_note +=1
        else:
            result.append(None)
    return result,count_note

def generate_lead (config):
    root_note = config["root_note"]
    scale = get_key(config["scale"])
    mask = get_mask_l(config["mask"])
    steps = config["steps"]
    oct_shift = config["oct_shift"]

    result=[]
    count_note=0
    for i in range(steps):
        scale_idx = i%len(scale)
        mask_idx = i%len(mask)

        note = root_note + scale[scale_idx] + oct_shift
        if mask[mask_idx] == 1:
            result.append(note)
            count_note +=1
        else:
            result.append(None)
    return result, count_note

if __name__ == "__main__":
        bass_config={
            "root_note" : 36,
            "scale" : "minor",
            "mask" : "power",
            "steps" : 16,
            "oct_shift" : 0
            }
        notes, count = generate_bass(bass_config)
        print("Бас: ",notes)
        print("Всего нот: ",count)
        
def midi_to_name(midi):
    note = NOTES[midi % 12]
    octave = midi // 12 - 1
    return f"{note}{octave}"


def generate_visual(notes, title,steps, note_color='#ff8800'):
    cols, rows = LAYOUT[steps]

    cell_size = 50
    intervals = 8
    top_margin = 80
    label_height = 25
    bottom_margin = 20

    width = cols*(cell_size + intervals) + intervals
    height = top_margin + rows*(cell_size + intervals + label_height) + intervals

    img = Image.new("RGB", (width, height), color="#2a2a2a")
    draw = ImageDraw.Draw(img)

    font_title = ImageFont.truetype("impact.ttf", 34)
    font_label = ImageFont.truetype("impact.ttf", 14)
    font_note = ImageFont.truetype("impact.ttf", 18)

    draw.text((10,10), title, fill="red", font=font_title)

    dot_radius = 3
    dot_y = top_margin - 12
    for step in [0,4,8,12]:
        x_center = intervals + step * (cell_size + intervals)+ cell_size //2
        draw.ellipse(
            [x_center - dot_radius, dot_y - dot_radius, x_center + dot_radius, dot_y + dot_radius],
            fill = "white"
        )
    for row_index in range(rows):
        start = row_index * cols
        end = start + cols
        row_notes = notes[start:end]

        y = top_margin + row_index * (cell_size + intervals + label_height)

        for col_idx in range(cols):
            x = intervals + col_idx * (cell_size + intervals)
            note = row_notes[col_idx]

            if note is None:
                color = "#444444"
                text = ""
            else:
                color = note_color
                text = midi_to_name(note)

            draw.rectangle(
                [x, y, x + cell_size, y + cell_size],
                fill=color, outline="#666666", width=2
            )

            if text:
                space = draw.textbbox((0, 0), text, font=font_note)
                text_width = space[2] - space[0]
                text_height = space[3] - space[1]
                text_x = x + (cell_size - text_width) // 2
                text_y = y + (cell_size - text_height) // 2 - 2
                draw.text((text_x, text_y), text, fill="white", font=font_note)

        label = f"steps {start + 1}-{end}"
        draw.text((intervals, y + cell_size + 5), label, fill="white", font=font_label)

    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer


