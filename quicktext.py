from groq import Groq
import streamlit as st
import datetime
import pandas as pd

# 🔑 API Key
client = Groq(api_key="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")

# 🌍 Imposta interfaccia
st.set_page_config(page_title="QuickText AI", page_icon="🧠")
st.title("🧠 QuickText AI con LLaMA3")
st.write("Genera testi creativi multilingua — powered by Groq")

# 📥 Input
text_type = st.selectbox("Tipo di testo", [
    "Bio Instagram", "Post motivazionale", "Descrizione prodotto", "Email professionale", "Altro"
])

user_input = st.text_area("📌 Scrivi una breve descrizione del contenuto")

tone = st.selectbox("🎭 Tono del testo", [
    "Professionale", "Divertente", "Amichevole", "Persuasivo", "Casuale"
])

language = st.selectbox("🌐 Lingua", ["Italiano", "Inglese", "Spagnolo"])

model = st.selectbox("🤖 Modello AI", [
    "llama3-8b-8192",
    "llama3-70b-8192"
])

# 💬 Prompt e system in base alla lingua
system_prompts = {
    "Italiano": "Sei un copywriter professionista italiano. Rispondi sempre in italiano.",
    "Inglese": "You are a professional English copywriter. Always reply in English.",
    "Spagnolo": "Eres un redactor publicitario profesional en español. Responde siempre en español."
}

def genera_prompt(tipo, contenuto, tono, lingua):
    return f"Scrivi in {lingua.lower()}. Scrivi un {tipo.lower()} con tono {tono.lower()} basato su questo input: {contenuto}"

# 🧠 Generazione
if st.button("🎨 Genera testo"):
    if not user_input.strip():
        st.warning("❗ Inserisci qualcosa per generare.")
    else:
        with st.spinner("✨ Sto generando il tuo testo..."):

            prompt = genera_prompt(text_type, user_input, tone, language)

            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompts[language]},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=300
            )

            output_text = response.choices[0].message.content.strip()

            # ✅ Mostra risultato
            st.success("✅ Testo generato con successo!")
            st.text_area("📄 Testo generato:", value=output_text, height=200)

            st.code(output_text, language='text')

            # 💾 Log in TXT
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open("log.txt", "a", encoding="utf-8") as f:
                f.write(
                    f"\n---\n🕒 {timestamp}\n🌍 Lingua: {language}\n📌 Tipo: {text_type}\n🎯 Tono: {tone}\n🤖 Modello: {model}\n✏️ Input: {user_input}\n📝 Output:\n{output_text}\n"
                )

            # 💾 Log in CSV
            df = pd.DataFrame([{
                "Timestamp": timestamp,
                "Lingua": language,
                "Tipo": text_type,
                "Tono": tone,
                "Modello": model,
                "Input": user_input,
                "Output": output_text
            }])
            try:
                df.to_csv("log.csv", mode='a', header=not pd.read_csv("log.csv").empty, index=False)
            except:
                df.to_csv("log.csv", mode='a', header=True, index=False)

            # 📎 Download .txt
            file_name = f"testo_generato_{timestamp.replace(':', '-')}.txt"
            st.download_button("📥 Scarica come .txt", output_text, file_name=file_name, mime="text/plain")
