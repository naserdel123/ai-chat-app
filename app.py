import os
import logging
from flask import Flask, request, jsonify, render_template
from openai import OpenAI

# Setup logging so errors appear clearly in Render logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Validate API key at startup
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    logger.error("❌ OPENAI_API_KEY environment variable is missing!")

# Create client lazily to avoid crash at import time
def get_client():
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is not set. Please add it in Render → Environment Variables.")
    return OpenAI(api_key=key)

conversation_history = []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/health")
def health():
    key = os.environ.get("OPENAI_API_KEY")
    return jsonify({
        "status": "ok",
        "api_key_set": bool(key),
        "api_key_prefix": key[:8] + "..." if key else "NOT SET"
    })

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON body"}), 400

        user_message = data.get("message", "").strip()
        if not user_message:
            return jsonify({"error": "Message is required"}), 400

        client = get_client()
        conversation_history.append({"role": "user", "content": user_message})

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "أنت مساعد ذكاء اصطناعي متقدم، ذكي، ودود ومفيد جداً. "
                        "تجيب باللغة التي يكتب بها المستخدم. "
                        "ردودك واضحة، مفيدة، ومفصّلة عند الحاجة."
                    ),
                },
                *conversation_history,
            ],
            max_tokens=2048,
            temperature=0.7,
        )
        assistant_message = response.choices[0].message.content
        conversation_history.append({"role": "assistant", "content": assistant_message})
        return jsonify({"response": assistant_message})

    except ValueError as e:
        logger.error(f"Config error: {e}")
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        logger.error(f"Chat error: {e}", exc_info=True)
        return jsonify({"error": f"حدث خطأ: {str(e)}"}), 500


@app.route("/image", methods=["POST"])
def generate_image():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON body"}), 400

        prompt = data.get("prompt", "").strip()
        style  = data.get("style", "realistic")

        if not prompt:
            return jsonify({"error": "Prompt is required"}), 400

        style_prompts = {
            "realistic":  f"{prompt}, photorealistic, ultra-detailed, 8K resolution, professional photography, cinematic lighting",
            "anime":      f"{prompt}, anime style, vibrant colors, detailed anime illustration, Studio Ghibli inspired, beautiful artwork",
            "animation":  f"{prompt}, 3D animation style, Pixar-like, cinematic, vibrant colors, ultra detailed, magical atmosphere",
        }
        enhanced_prompt = style_prompts.get(style, style_prompts["realistic"])

        client = get_client()
        response = client.images.generate(
            model="dall-e-3",
            prompt=enhanced_prompt,
            size="1024x1024",
            quality="hd",
            n=1,
        )
        image_url = response.data[0].url
        return jsonify({"image_url": image_url, "revised_prompt": response.data[0].revised_prompt})

    except ValueError as e:
        logger.error(f"Config error: {e}")
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        logger.error(f"Image error: {e}", exc_info=True)
        return jsonify({"error": f"حدث خطأ: {str(e)}"}), 500


@app.route("/clear", methods=["POST"])
def clear_history():
    global conversation_history
    conversation_history = []
    return jsonify({"status": "cleared"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
