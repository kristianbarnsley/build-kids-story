import streamlit as st
from textgeneration import *

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
        intro = generateIntro(name, gender, len(selected_countries))
        st.text(intro)
        i=0
        animal_intro_sections = []
        for country in selected_countries:
            animal_intro = getAnimalIntro(st.session_state.animal_selections[country], name, country, st.session_state.value_selections[country], i)
            animal_intro_sections.append(animal_intro)
            st.text(animal_intro)
            i += 1
        lost_text = getLost(name)
        st.text(lost_text)
        story_so_far = intro
        for section in animal_intro_sections:
            story_so_far = story_so_far + section
        story_so_far = story_so_far + lost_text
        st.text(getEnding(name, story_so_far))