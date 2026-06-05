import streamlit as st
import anthropic

st.title("Claude Console")
st.write("Enter your prompt below to interact with Claude via the API.")

# Get API key from Streamlit secrets
api_key = st.secrets.get("ANTHROPIC_API_KEY", "")

if not api_key:
      st.warning("Please set your ANTHROPIC_API_KEY in Streamlit secrets.")
else:
      client = anthropic.Anthropic(api_key=api_key)

    model = st.selectbox(
              "Model",
              ["claude-opus-4-5", "claude-sonnet-4-5", "claude-haiku-3-5"],
              index=1,
    )

    user_input = st.text_area("Your prompt:", height=200)

    if st.button("Send") and user_input:
              with st.spinner("Thinking..."):
                            message = client.messages.create(
                                              model=model,
                                              max_tokens=2048,
                                              messages=[{"role": "user", "content": user_input}],
                            )
                            response = message.content[0].text
                        st.subheader("Response")
        st.write(response)
