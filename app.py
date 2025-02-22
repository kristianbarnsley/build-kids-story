import streamlit as st
from openai import OpenAI
import os
import json
from dotenv import load_dotenv


load_dotenv()
#OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
MODEL="gpt-4o"
client = OpenAI(api_key=OPENAI_API_KEY)

def queryLLM(query, system_prompt, client, json=False):
    if json == True:
        response = client.chat.completions.create(
            model=MODEL,
            response_format ={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ],
            temperature=0.6,
        )
    else:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ],
            temperature=0.6,
        )
    return response.choices[0].message.content

def getAnimals(country, client):
    prompt = f"""Give me a list of 3 cultrally significant animals to the country of {country}. The animals can be real or mythological. These animals should be suitible to be charaters in a kids book. 
    Reply only with a list of animals in list spereated by commas and using no quotation marks or underscores, such as: Animal1, Animal2, Animal3"""
    system_prompt = "You are an AI assistant helping write a kids book"
    response = queryLLM(query=prompt, system_prompt=system_prompt, client=client)
    response = response.split(", ")
    return response

def getValues(country, client):
    prompt = f"""Give me a list of 3 cultrally significant values to the country of {country}. The values should be important things that the large majority of people from {country} resonate with and 
    would want to share with their child. These values should be suitible to be explained in a kids book and at some point will be used to overcome challenges the child in the book faces while lost in 
    the forest. Reply only with a list of values in list spereated by commas and using no quotation marks or underscores, such as: Value1, Value2, Value3"""
    system_prompt = "You are an AI assistant helping write a kids book"
    response = queryLLM(query=prompt, system_prompt=system_prompt, client=client)
    response = response.split(", ")
    return response

st.set_page_config(page_title="Build your own story!")

# Initialize session state variables
if "step" not in st.session_state:
    st.session_state.step = 1

if "animal_results" not in st.session_state:
    st.session_state.animal_results = {}

if "value_results" not in st.session_state:
    st.session_state.value_results = {}

if "animal_selections" not in st.session_state:
    st.session_state.animal_selections = {}

if "value_selections" not in st.session_state:
    st.session_state.value_selections = {}

if st.session_state.step >= 1:
    name = st.text_input("Enter a name:")
    gender = st.radio("Select a gender:", ["Male", "Female"])
    countries = [
        "China", "India", "United States", "Indonesia", "Pakistan",
        "Brazil", "Nigeria", "Bangladesh", "Russia", "Mexico",
        "Japan", "France", "Philippines", "Egypt", "Vietnam",
        "United Kingdom", "Turkey", "Iran", "Germany", "Thailand"
    ]
    countries.sort()
    selected_countries = st.multiselect(
        "Select up to 4 countries:",
        countries,
        max_selections=4
    )

animals_values_generated = False

if st.button("Suggest National Animals and Values"):
    if selected_countries:
        
        animal_results = {}
        value_results = {}
        for i in range(0, len(selected_countries)):
            animals = getAnimals(selected_countries[i], client)
            animal_results[selected_countries[i]] = animals
            values = getValues(selected_countries[i], client)
            value_results[selected_countries[i]] = values
        st.session_state.animal_results = animal_results
        st.session_state.value_results = value_results
        st.session_state.step = max(st.session_state.step, 2)
        #st.write("Suggested Animals:", animal_results)
        #st.write("Suggested Values:", value_results)
    else:
        st.write("No countries selected yet")

if st.session_state.step >= 2:
        for i in range(0, len(selected_countries)):
            st.write(f"{selected_countries[i]}")
            st.session_state.animal_selections[selected_countries[i]] = st.pills(f"Animal for {selected_countries[i]}", st.session_state.animal_results[selected_countries[i]], selection_mode="single")
            st.session_state.value_selections[selected_countries[i]] = st.pills(f"Value for {selected_countries[i]}", st.session_state.value_results[selected_countries[i]], selection_mode="single")
        if  all(st.session_state.animal_selections[country] for country in st.session_state.animal_selections.keys()) and all(st.session_state.value_selections[country] for country in st.session_state.value_selections.keys()):
            st.session_state.step = max(st.session_state.step, 3)

if st.session_state.step >= 3:
    if st.button("Generate Story!"):
        st.write("Placeholder")