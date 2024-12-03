import streamlit as st
from inference import MovieRecommendationSystem
import json

PINECONE_API_KEY = st.secrets["API_KEY"]["PINECONE"]
rec_sys = MovieRecommendationSystem(PINECONE_API_KEY)

st.header("Semantic movie search by Alican Kapusuz", divider="gray")
st.info("Search movies by describing what you want to watch. You can focus on plot, setting, genre etc. For inspiration check out the examples under 'Choose a query' or write your own by choosing Custom query!", icon="ℹ️")
st.info("Currently we only have IMDB top 250 movies from a couple of years ago so the ratings might be slightly different now.", icon="ℹ️")

with open("./example.json", 'r') as file:
    examples = json.load(file)

access_code = st.text_input("Enter your access code to use this app:")

selected_example = st.selectbox("Choose a query:", ["Custom query"] + [example["query"] for example in examples])

# Text input for query
if selected_example is not None and selected_example != "Custom query":
    query_input = st.text_area(
        "Enter your query:", value=selected_example, key="example_input"
    )
    selected_result = next(
        example["result"]
        for example in examples
        if example["query"] == selected_example
    )
else:
    query_input = st.text_area("Enter your query:", key="custom_input")
    selected_result = None

# Display output
if st.button("Recommend"):
    if selected_result:
        st.write(f"### Example Query: {selected_example}")
        st.write("### Example Recommendations:")
        for match in selected_result["matches"]:
            st.write(
                f"- **Title:** [{match['metadata']['title']}]({match['metadata']['link']}) "
                f"({int(match['metadata']['year'])}) - Rating: {match['metadata']['rating']} "
                f"(Score: {match['score']:.2f})"
            )
    elif access_code.lower()==st.secrets["ACCESS"]["CODE"]:
        if len(query_input) > 0:
            results = rec_sys.query(query_input)
            for match in results["matches"]:
                st.write(
                    f"- **Title:** [{match['metadata']['title']}]({match['metadata']['link']}) "
                    f"({int(match['metadata']['year'])}) - Rating: {match['metadata']['rating']} "
                    f"(Score: {match['score']:.2f})"
                )
        else:
            st.write("Query field seems to be empty, please try again :(")
    else:
        st.write("Your access code is not working. Try again and make sure Custom query is chosen. If it still doesn't work, please contact alican.kapusuz@outlook.com")