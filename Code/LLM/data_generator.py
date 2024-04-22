import random
import math
import string
import shelve
import inflect
from transformers import T5ForConditionalGeneration, T5Tokenizer
from Code.walker import COLORS, MOVEMENTS

def data_for_simulation(
        num_walkers: int, num_barriers: int, num_portals: int, num_mudspots: int) -> dict:
    """
    This function generates data for the graphing of the simulation.
    """
    data = {"Walkers": [], "Barriers": [], "Portals": [], "Mudspots": []}
    for _ in range(num_walkers):
        data["Walkers"].append({"movement": random.choice([key for key in MOVEMENTS.keys()]),
                                "color": random.choice(COLORS),
                                "location": (round(random.uniform(-100, 100),2), round(random.uniform(-100, 100),2))})
    for _ in range(num_barriers):
        data["Barriers"].append({"center": (round(random.uniform(-100, 100),2), round(random.uniform(-100, 100),2)),
                                 "length": round(random.uniform(0, 50),2),
                                 "angle": round(random.uniform(0, 2 * math.pi),4)})
    for _ in range(num_portals):
        data["Portals"].append({"center": (round(random.uniform(-100, 100),2), round(random.uniform(-100, 100),2)),
                                "radius": round(random.uniform(0, 10),2),
                                "endpoint": (round(random.uniform(-100, 100),2), round(random.uniform(-100, 100),2))})
    for _ in range(num_mudspots):
        data["Mudspots"].append({"bottom_left": (round(random.uniform(-100, 100),2), round(random.uniform(-100, 100),2)),
                                 "height": round(random.uniform(0, 50),2),
                                 "width": round(random.uniform(0, 50),2)})
    return data

def simulation_variables() -> tuple[dict,dict]:
    """
    This function generates the variables for the simulation.
    """
    letters = string.ascii_lowercase
    filename = ''.join(random.choice(letters) for i in range(6))
    iterations = random.randint(1, 10)
    buffer = random.randint(1, 100)
    n = random.randint(1, 1000)
    steps = random.randint(3, 14)
    gravity = random.choice([1, 0, -1])
    graphing_data = {"type": "graph",
                    "iterations": iterations,
                    "max_depth": n+buffer,
                    "n": n,
                    "steps": n/steps,
                    "filename": f"./{filename}"}
    plottings_data = {"type": "plot",
                      "n": n,
                      "gravity": gravity,
                      "filename": f"./{filename}"}
    return graphing_data, plottings_data

def generate_data() -> tuple[dict, dict]:
    """
    This function generates data for the simulation.
    """
    graphing_data, plottings_data = simulation_variables()
    data = data_for_simulation(random.randint(1, 7), random.randint(0, 5),
                                random.randint(0, 5), random.randint(0, 5))
    graphing = data
    graphing["Simulation"] = graphing_data
    plotting = data
    plotting["Simulation"] = plottings_data
    return (graphing, plotting)

def save_data(size: int, filename: str = "data.json") -> None:
    """
    This function saves the data to a JSON file.
    """
    for _ in range(0,size,2):
        with shelve.open(filename) as shelve_file:
            data_1, data_2 = generate_data()
            shelve_file[create_description(data_1)], shelve_file[create_description(data_2)] = data_1, data_2
            shelve_file.sync()

def create_description(data: dict) -> str:
    """
    This function creates a description for the simulation.
    """
    p = inflect.engine()
    description = "I want to simulate"
    for key, value in data.items():
        if key == "Simulation":
            continue
        description += f" {len(value)} {key}, "
        for index, item in enumerate(value):
            if key == "Walkers":
                description += f"The {p.ordinal(index + 1)} {key[:-1].lower()} \
should start at {item['location']}, \
move in a {MOVEMENTS[item['movement']]}, and be colored {item['color']}.\n"
            elif key == "Barriers":
                description += f"The {p.ordinal(index + 1)} {key[:-1].lower()} \
should be centered at {item['center']}, \
have a length of {item['length']}, and be at an angle of {item['angle']}.\n"
            elif key == "Portals":
                description += f"The {p.ordinal(index + 1)} {key[:-1].lower()} \
should be centered at {item['center']}, \
have a radius of {item['radius']}, and lead to {item['endpoint']}.\n"
            elif key == "Mudspots":
                description += f"The {p.ordinal(index + 1)} {key[:-1].lower()} \
should start from {item['bottom_left']} (bottom left), \
have a height of {item['height']}, and a width of {item['width']}.\n"
        description += "\n"
    description = description.rstrip(', ')
    return description

def paraphrase(paragraph: str) -> str:
    """
    This function paraphrases the paragraph.
    """
    new_paragraph = ""
    for sentence in paragraph.split("\n"):
        new_paragraph += paraphrase_sentence(sentence) + "\n"
    return new_paragraph

def paraphrase_sentence(sentence: str) -> str:
    """
    This function creates a paraphrase of the given sentence.
    """
    # Initialize the tokenizer and model
    tokenizer = T5Tokenizer.from_pretrained('t5-3b')
    model = T5ForConditionalGeneration.from_pretrained('t5-3b')

    for word in sentence.split(" "):
        print(is_word_in_vocab(word, tokenizer), word)
    # Prepare the sentence for T5
    text = "paraphrase: " + sentence

    # Encode the sentence and generate a response
    encoding = tokenizer.encode_plus(text, return_tensors='pt')
    output = model.generate(**encoding, max_length=300, num_return_sequences=1, temperature=1.1)

    # Decode the response
    paraphrased = tokenizer.decode(output[0], skip_special_tokens=True)

    return paraphrased

def print_data(path: str) -> None:
    """
    This function prints the data from the file.
    """
    with shelve.open(path) as shelve_file:
        for key, item in shelve_file.items():
            print(f"{key}:\n{item}\n")

def is_word_in_vocab(word: str, tokenizer: T5Tokenizer) -> bool:
    """
    This function checks if a word is in the tokenizer's vocabulary.
    """
    vocab = tokenizer.get_vocab()
    return word in vocab
