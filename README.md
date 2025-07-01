#  Video Script Generator with TTS and Background Audio

This project automatically generates video scripts from a topic or keyword, converts the script to natural speech using TTS, and mixes it with optional background music and sound effects.

---

## Features

###  Script Generation
- Automated topic research from Google
- Dynamic script structure with intro, body, and call to action
- Multiple video lengths: short, medium, long
- Templated script formatting

###  Voice Generation
- Text-to-speech with Microsoft Edge TTS
- Multiple voice options
- Adjustable speaking rate
- Future-ready for emotion control (styles)

###  Audio Production
- Optional background music support (MP3/WAV)
- Sound effects support (WAV)
- Auto-mixing of voice, music, and effects
- Clean WAV output with timestamped filenames

---

##  Requirements

- Python 3.8+
- ffmpeg installed and added to PATH
- Internet connection (for TTS and Google topics)
- Dependencies (see below)

---

##  Installation

```bash
git clone https://github.com/monu20050608/video-script-generator.git
cd video-script-generator
python -m venv venv
venv\Scripts\activate    # or source venv/bin/activate on Linux/macOS
pip install -r requirements.txt

 Environment Setup

Create a .env file and add your SerpAPI key:

SERPAPI_KEY=your_serpapi_key_here

    Or set it in your system environment variables.

 Usage
🔸 Generate a script with a topic:

python main.py --topic "Blockchain Technology"

🔸 Or search Google for ideas:

python main.py --query "Latest tech trends"

🔸 Add background music and SFX:

python create_background_music.py

python create_beep_sfx.py

python main.py --topic "AI in Healthcare" --music background.wav --sfx sfx/beep.wav --sfx_position 3000

📂 Output

All generated files are saved in the /outputs/ folder:

    *_script.txt – the generated script

    *_voice.wav – TTS audio

    *_final_mix.wav – mixed voice + music + SFX

🧪 Testing Helpers

Use the included scripts to generate dummy files:

python create_beep_sfx.py           # Creates sfx/beep.wav
python create_background_music.py   # Creates background.wav

🎯 Roadmap

Emotion style support (style=cheerful, sad, etc.)

Voice cloning (Coqui TTS)

Export to MP3

Storyboard generation

    GUI version

🧠 Resources

    Coqui TTS

    Edge-TTS

    SerpAPI

    Free Music & SFX

👨‍💻 Created By

Chaman Yadav
