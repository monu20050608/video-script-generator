# main.py
import os
import argparse
import asyncio
from datetime import datetime
from pydub import AudioSegment

# ---- CONFIGURATION ----
OUTPUT_DIR = "outputs"
DEFAULT_VOICE = "en-US-AriaNeural"
DEFAULT_LENGTH = "medium"
DEFAULT_LANGUAGE = "en"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ---- TOPIC FETCHING (SERPAPI) ----
def get_google_topics(query):
    try:
        from serpapi import GoogleSearch
    except ImportError:
        raise ImportError("Install SerpAPI with: pip install google-search-results")

    serpapi_key = os.getenv("322587b4105c9159069be1bf976106de70331c72a6ef5f30e18157c2fd7ca46d")

    params = {
        "api_key": serpapi_key,
        "engine": "google",
        "q": query,
        "num": "5"
    }
    search = GoogleSearch(params)
    results = search.get_dict()

    topics = []
    for res in results.get("organic_results", []):
        title = res.get("title", "No Title")
        snippet = res.get("snippet", "In today’s video, we’re diving deep into the world.")
        topics.append({"title": title, "snippet": snippet})
    return topics

# ---- SCRIPT GENERATION ----
def generate_script(topic_info, length="medium", language="en"):
    title = topic_info["title"]
    snippet = topic_info["snippet"]

    return (
        f"Video Script for '{title}'\n\n"
        f"Welcome! Today we will explore: {title}\n\n"
        f"In today’s video, we’re diving deep into the world of {title}. This subject is becoming increasingly important in our lives, and understanding it can give you a major advantage.\n\n"
        f"Whether you're a beginner or someone looking to expand your knowledge, this video will break it down in a simple and easy-to-follow way.\n\n"
        f"We’ll cover what {title} is, why it matters, how it’s used in real life, and what you need to know going forward.\n\n"
        f"{title} has been gaining a lot of attention recently, and for good reason. It offers unique opportunities and poses interesting challenges that everyone should be aware of.\n\n"
        f"We’ll also explore some practical examples and case studies to help you see how {title} works in real-world situations.\n\n"
        f"By understanding the key concepts and ideas behind {title}, you’ll be able to make more informed decisions and confidently discuss this topic with others.\n\n"
        f"Finally, we’ll share a few tips and resources you can use to continue learning about {title} and stay up to date with the latest developments.\n\n"
        f"By the end of this video, you’ll have a solid understanding of {title} and how it can impact your decisions, work, or daily life."
        "This topic is important because it helps you stay informed and make better decisions.\n\n"
        "Subscribe and follow for more videos.\n\n"
        "Created by Chaman Yadav \n\n"
    )

# ---- EDGE TTS GENERATION ----
async def generate_voice_edge_async(text, output_path, voice, style=None, rate=None):
    import edge_tts

    communicate = edge_tts.Communicate(text=text, voice=voice)
    save_kwargs = {}
    if style:
        save_kwargs["style"] = style
    if rate:
        save_kwargs["rate"] = rate

    await communicate.save(output_path, **save_kwargs)

def generate_voice_edge(text, output_path, voice, style=None, rate=None):
    asyncio.run(generate_voice_edge_async(text, output_path, voice, style, rate))

# ---- AUDIO MIXING ----
def mix_audio(voice_path, music_path, output_path, music_volume=-20, sfx_path=None, sfx_position=5000):
    voice = AudioSegment.from_file(voice_path)
    music = AudioSegment.from_file(music_path).apply_gain(music_volume)
    combined = music.overlay(voice)

    if sfx_path:
        sfx = AudioSegment.from_file(sfx_path)
        combined = combined.overlay(sfx, position=sfx_position)

    combined.export(output_path, format="wav")

# ---- MAIN ----
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Video Script Generator with TTS, Music, and SFX")
    parser.add_argument("--query", help="Search query to fetch topics from Google")
    parser.add_argument("--topic", help="Single topic (overrides --query if provided)")
    parser.add_argument("--length", default=DEFAULT_LENGTH, choices=["short", "medium", "long"], help="Script length")
    parser.add_argument("--voice", default=DEFAULT_VOICE, help="Edge TTS voice (e.g., en-US-AriaNeural)")
    parser.add_argument("--language", default=DEFAULT_LANGUAGE, help="Script language")
    parser.add_argument("--music", help="Optional background music file (mp3/wav)")
    parser.add_argument("--style", help="Voice style")
    parser.add_argument("--rate", help="Voice rate")
    parser.add_argument("--sfx", help="Optional sound effect file (mp3/wav)")
    parser.add_argument("--sfx_position", type=int, default=5000, help="Position to overlay SFX in ms")
    args = parser.parse_args()

    topics = []
    if args.topic:
        print(f"🔍 Fetching description for topic: {args.topic}")
        try:
            search_results = get_google_topics(args.topic)
            if search_results:
                snippet = search_results[0]["snippet"]
            else:
                snippet = "No description available."
        except Exception as e:
            print(f"❌ Error fetching topic description: {e}")
            snippet = "No description available."
        topics = [{"title": args.topic, "snippet": snippet}]
    elif args.query:
        print(f"🔍 Fetching topics for query: {args.query}")
        try:
            topics = get_google_topics(args.query)
        except Exception as e:
            print(f"❌ Error fetching topics: {e}")
            exit(1)

        if not topics:
            print("⚠️ No topics found.")
            exit(1)
    else:
        print("⚠️ You must specify either --topic or --query.")
        exit(1)

    for topic_info in topics:
        title_safe = topic_info["title"].replace(" ", "_").replace("/", "_")[:20]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = f"{timestamp}_{title_safe}"

        print(f"\n🎬 Generating script for: {topic_info['title']}")
        script_text = generate_script(topic_info, args.length, args.language)

        script_path = os.path.join(OUTPUT_DIR, f"{base_name}_script.txt")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(script_text)
        print(f"✅ Script saved: {script_path}")

        audio_path = os.path.join(OUTPUT_DIR, f"{base_name}_voice.wav")
        print(f"🔊 Generating TTS audio...")
        try:
            generate_voice_edge(script_text, audio_path, args.voice, args.style, args.rate)
        except Exception as e:
            print(f"❌ TTS generation failed: {e}")
            continue
        print(f"✅ Audio saved: {audio_path}")

        if args.music:
            final_path = os.path.join(OUTPUT_DIR, f"{base_name}_final_mix.wav")
            print(f"🎵 Mixing with background music and SFX...")
            try:
                mix_audio(
                    audio_path,
                    args.music,
                    final_path,
                    sfx_path=args.sfx,
                    sfx_position=args.sfx_position
                )
            except Exception as e:
                print(f"❌ Audio mixing failed: {e}")
                continue
            print(f"✅ Final mixed audio saved: {final_path}")

    print("\n✅ All done!")
