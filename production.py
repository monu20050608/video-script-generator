def create_timestamp_markers(script_text, sec_per_line=5):
    lines = [line for line in script_text.split("\n") if line.strip()]
    timestamps = []
    time = 0
    for line in lines:
        timestamps.append((time, line))
        time += sec_per_line
    return timestamps

def suggest_b_roll(topic):
    return [
        f"{topic} stock footage",
        f"{topic} diagrams",
        "Presenter speaking",
        "Animations or infographics",
    ]

def scene_descriptions(script_text):
    sections = script_text.split("\n\n")
    return [f"Scene {i+1}: {section[:50]}..." for i, section in enumerate(sections)]
