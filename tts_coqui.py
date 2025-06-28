from TTS.api import TTS

def generate_voice_coqui(
    text,
    output_path,
    model_name="tts_models/en/ljspeech/tacotron2-DDC",
    speed=1.0,
):
    tts = TTS(model_name=model_name)
    tts.tts_to_file(
        text=text,
        file_path=output_path,
        speed=speed,
    )
    print(f"Coqui TTS audio saved to {output_path}")

