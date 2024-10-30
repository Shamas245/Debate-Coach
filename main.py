import openai
import streamlit as st
from streamlit_chat import message
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
openai.api_key = st.secrets("OPENAI_API_KEY")

class DebateHelper:
    """A class that provides debate and declamation assistance."""

    def __init__(self):
        # Initialize conversation history
        if "conversation_history" not in st.session_state:
            st.session_state.conversation_history = []
        
    def generate_response(self, messages, max_tokens=700, temperature=0.7):
        """General method to request a response from the OpenAI API."""
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            max_tokens=max_tokens,
            temperature=temperature,
            messages=messages,
            stream=True
        )
        response_container = st.empty()  # Placeholder for progressive response display
        full_response = ""
        
        # Stream response in real time, update only in this loop
        for chunk in response:
            if 'content' in chunk['choices'][0]['delta']:
                chunk_text = chunk['choices'][0]['delta']['content']
                full_response += chunk_text
                response_container.write(full_response)  # Update placeholder with new text
        
        return full_response.strip()  # Return final response only, without re-displaying it

    def generate_declamation_content(self, topic, level):
        """Generate sample declamation content based on topic and level."""
        messages = [
            {"role": "system", "content": "Provide declamation guidance and a sample two-paragraph response."},
            {"role": "user", "content": f"Topic: {topic}. Complexity level: {level}."}
        ]
        return self.generate_response(messages)

    @staticmethod
    def get_parliamentary_rules():
        """Returns rules for Parliamentary Debate."""
        return (
            "Parliamentary Debate Rules:\n"
            "1. Debate is split into government and opposition teams.\n"
            "2. Each speaker has a time limit for arguments.\n"
            "3. Formal language is required; no direct addresses.\n"
            "4. Constructive speeches and rebuttals are key.\n"
            "5. Maintain decorum and follow the speaker's instructions."
        )

    @staticmethod
    def get_mun_rules():
        """Returns rules for Model United Nations (MUN)."""
        return (
            "Model United Nations (MUN) Rules:\n"
            "1. Delegates represent assigned countries.\n"
            "2. Use formal language and courtesy.\n"
            "3. Follow parliamentary procedures.\n"
            "4. Propose resolutions and debate global issues.\n"
            "5. Vote on resolutions after debate."
        )

    def add_to_history(self, role, content):
        """Add a message to the conversation history."""
        st.session_state.conversation_history.append({"role": role, "content": content})

    def display_history(self):
        """Display conversation history in chat format."""
        st.write("### Conversation History")
        for entry in st.session_state.conversation_history:
            message(entry["content"], is_user=(entry["role"] == "User"))

    def parliamentary_practice(self):
        """Parliamentary Debate practice interface."""
        st.write("### Parliamentary Debate Rules")
        st.write(self.get_parliamentary_rules())
        
        motives = st.text_input("Enter your motives for discussion:")
        if motives:
            response = self.generate_response([
                {"role": "user", "content": f"As a debater, your motives are: '{motives}'. Suggest an approach to argue this effectively."}
            ])
            
            self.add_to_history("Coach", response)

    def mun_practice(self):
        """Model United Nations (MUN) practice interface."""
        st.write("### Model United Nations (MUN) Rules")
        st.write(self.get_mun_rules())
        
        stance = st.text_input("Enter your country or organization's stance on a global issue:")
        if stance:
            response = self.generate_response([
                {"role": "user", "content": f"In an MUN session, the user represents a country with the stance: '{stance}'. Generate points to support this stance and suggest diplomatic language."}
            ])
            
            self.add_to_history("Coach", response)

    def declamation_practice(self):
        """Declamation preparation interface."""
        st.markdown("### 📝 Declamation Preparation")
        topic = st.text_input("💡 Enter the topic of your declamation:")
        level = st.selectbox("Select your level:", ["Low", "Medium", "High"])

        if st.button("Generate Declamation") and topic and level:
            content = self.generate_declamation_content(topic, level.lower())
            self.add_to_history("User", topic)
            self.add_to_history("Coach", content)

class DebateApp:
    """Main application class for Debate Helper."""

    def __init__(self):
        self.helper = DebateHelper()

    def run(self):
        """Main application logic."""
        st.title("🗣️ Debate Coach")
        st.subheader("Welcome to the Ultimate Debate Companion!")
        st.write("👋 Choose your debate style below to start your journey in mastering debate.")
        st.markdown("---")

        debate_style = st.selectbox(
            "🎓 Select Debate Style",
            options=["Select", "Declamation", "Parliamentary Debate", "Model United Nations"]
        )

        if debate_style == "Declamation":
            self.helper.declamation_practice()

        elif debate_style == "Parliamentary Debate":
            self.helper.parliamentary_practice()

        elif debate_style == "Model United Nations":
            self.helper.mun_practice()

        # Display the conversation history
        self.helper.display_history()

if __name__ == "__main__":
    app = DebateApp()
    app.run()
