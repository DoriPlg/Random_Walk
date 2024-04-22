import random
import math
import string
import torch
import shelve
import inflect
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
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

def describe_walker(walker: dict) -> str:
    """
    This function creates a description for the walker.
    """
    return f"walker should start at {walker['location']}, \
move in a {MOVEMENTS[walker['movement']]}, and be colored {walker['color']}"
def describe_barrier(barrier: dict) -> str:
    """
    This function creates a description for the barrier.
    """
    return f"barrier should be centered at {barrier['center']}, \
have a length of {barrier['length']}, and be at an angle of {barrier['angle']}"
def describe_portal(portal: dict) -> str:
    """
    This function creates a description for the portal.
    """
    return f"portal should be centered at {portal['center']}, \
have a radius of {portal['radius']}, and lead to {portal['endpoint']}"
def describe_mudspot(mudspot: dict) -> str:
    """
    This function creates a description for the mudspot.
    """
    return f"mudspot should start from {mudspot['bottom_left']} (bottom left), \
have a height of {mudspot['height']}, \
and a width of {mudspot['width']}"

def create_description(data: dict) -> str:
    """
    This function creates a description for the simulation.
    """
    p = inflect.engine()
    description = "I want to simulate"
    for key, value in data.items():
        if key == "Simulation":
            continue
            # Return here later
        description += f" {len(value)} {key}, "
        for index, item in enumerate(value):
            if key == "Walkers":
                description += \
                    f"The {p.ordinal(p.number_to_words(index + 1))} {describe_walker(item)}.\n"
            elif key == "Barriers":
                description += \
                    f"The {p.ordinal(p.number_to_words(index + 1))} {describe_barrier(item)}.\n"
            elif key == "Portals":
                description += \
                    f"The {p.ordinal(p.number_to_words(index + 1))} {describe_portal(item)}.\n"
            elif key == "Mudspots":
                description += \
                    f"The {p.ordinal(p.number_to_words(index + 1))} {describe_mudspot(item)}.\n"
    return description

def paraphrase(paragraph: str) -> list[str]:
    """
    This function paraphrases the paragraph.
    """
    new_paragraphs = []
    for sentence in paragraph.split("\n"):
        if len(sentence) == 0:
            continue
        phrases = paraphrase_sentence(sentence)
        updated_phrases = []
        for paragraph in new_paragraphs:
            for paraphrased in phrases:
                updated_phrases.append(paragraph + "\n" + paraphrased)
        if len(new_paragraphs) == 0:
            new_paragraphs = phrases
        else:
            new_paragraphs = updated_phrases
    return new_paragraphs

def paraphrase_sentence(sentence: str) -> list[str]:
    """
    This function creates a paraphrase of the given sentence.
    """
    # Initialize the tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained(
        "ramsrigouthamg/t5-large-paraphraser-diverse-high-quality")
    model= AutoModelForSeq2SeqLM.from_pretrained(
        "ramsrigouthamg/t5-large-paraphraser-diverse-high-quality")
    device = torch.device("cpu")
    model = model.to(device)

    # Prepare the sentence for T5
    text = "paraphrase:" + sentence + " </s>"

    # Encode the sentence and generate a response
    encoding = tokenizer.encode_plus(text,max_length =128, padding=True, return_tensors="pt")
    input_ids,attention_mask  = encoding["input_ids"].to(device), encoding["attention_mask"].to(device)
    model.eval()
    diverse_beam_outputs = model.generate(
        input_ids=input_ids,attention_mask=attention_mask,
        max_length=128,
        early_stopping=True,
        num_beams=3,
        num_beam_groups = 3,
        num_return_sequences=3,
        diversity_penalty = 0.70
    )

    # Decode the response
    paraphrased = []
    for beam_output in diverse_beam_outputs:
        sent = tokenizer.decode(beam_output, skip_special_tokens=True,clean_up_tokenization_spaces=True)
        paraphrased.append(sent.removeprefix("paraphrasedoutput: "))
    return paraphrased

def is_word_in_vocab(word: str, tokenizer: AutoTokenizer) -> bool:
    """
    This function checks if a word is in the tokenizer's vocabulary.
    """
    vocab = tokenizer.get_vocab()
    token_exists = True
    for subword in tokenizer.tokenize(word):
        if subword not in vocab:
            token_exists = False
            break
    return token_exists

def print_data(path: str) -> None:
    """
    This function prints the data from the file.
    """
    with shelve.open(path) as shelve_file:
        for key, item in shelve_file.items():
            print(f"{key}:\n{item}\n")
