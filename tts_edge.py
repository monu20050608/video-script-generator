import edge_tts

async def generate_voice_edge(
    text,
    output_path,
    voice="en-US-AriaNeural",
    rate="+0%",
    pitch="0%"
):
    communicate = edge_tts.Communicate(
        text=text,
        voice=voice,
        rate=rate,
        pitch=pitch,
    )
    await communicate.save(output_path)
