from openai import OpenAI
import streamlit as st

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
    would want to share with their child. If these values are not writen in english, you should proved an english translation in brackets. These values should be suitible to be explained in a kids book 
    and at some point will be used to overcome challenges the child in the book faces while lost in the forest. Reply only with a list of values in list spereated by commas and using no quotation 
    marks or underscores, such as: Value1, Value2, Value3"""
    system_prompt = "You are an AI assistant helping write a kids book"
    response = queryLLM(query=prompt, system_prompt=system_prompt, client=client)
    response = response.split(", ")
    return response

def generateIntro(name, gender, count):
    if gender == "Male":
        he_she_they = "he"
        him_her_them = "him"
        his_her_their = "his"
    if gender == "Female":
        he_she_they = "she"
        him_her_them = "her"
        his_her_their = "her"
    if count == 2:
        num_sections = "two"
    if count == 3:
        num_sections = "three"
    if count == 4:
        num_sections = "four"

    intro = f"""{name} skipped through the garden wide,
With flowers and trees on every side.
The sun peeked out, the sky was bright,
The birds sang sweet—a pure delight!

{he_she_they.capitalize()} watched a butterfly float and glide,
Then chased it near a tree so wide.
Past the pond, beyond the gate,
Through winding paths—was it getting late?

The breeze grew cool, the trees stood tall,
{his_her_their.capitalize()} house now seemed so very small.
Still, {he_she_they} wandered, step by step,
Through leafy trails where shadows crept.

Then, in the dirt, near mossy ground,
A golden shimmer twinkled round.
{name} bent down, {his_her_their} fingers brushed—
A magic medallion, covered in dust!

{he_she_they.capitalize()} picked it up and gave a blow,
The dust swirled off—a golden glow!
The medallion gleamed with colors bright,
It's {num_sections} sections, a world of light.

{name} whispered, “What could this be?”
The symbols shimmered, shifting free.
Then all at once, a breeze blew round,
And the earth began to hum and sound..."""
    return intro

def getAnimalIntro(animal, name, country, value, order):
    intro = f"""Name skipped through the garden wide,
With flowers and trees on every side.
The sun peeked out, the sky was bright,
The birds sang sweet—a pure delight!

They watched a butterfly float and glide,
Then chased it near a tree so wide.
Past the pond, beyond the gate,
Through winding paths—was it getting late?

The breeze grew cool, the trees stood tall,
Their house now seemed so very small.
Still, they wandered, step by step,
Through leafy trails where shadows crept.

Then, in the dirt, near mossy ground,
A golden shimmer twinkled round.
Name bent down, their fingers brushed—
A magic medallion, covered in dust!

They picked it up and gave a blow,
The dust swirled off—a golden glow!
The medallion gleamed with colors bright,
It's four sections, a world of light.

Name whispered, “What could this be?”
The symbols shimmered, shifting free.
Then all at once, a breeze blew round,
And the earth began to hum and sound..."""
    order_prompt = [
        "first",
        "second",
        "third",
        "fourth"
    ]
    prompt = f"""Come up with a short section of a kids book that introduces a magical {animal} than appears from a medallion and teaches a child called {name} 
    about the importance of {value} and how it's part of their heratige coming from {country}. This section should start by describing how the animal comes out 
    of the the {order_prompt[order]} section of the medallion. The animal should then introduce itself, providing it with a suitable name for {country}, the animal 
    should use a traditional greating in the countries language, but otherwise only speak in english. The animal should then explain that it is there to teach them 
    about {value} and breifly explain why it is important. This should all be done in 8 lines. Respond only with the section of the book, provide no other infomation or plesantries. 
    To help you write this section here is how the book starts, please write in a similar style: {intro}"""
    system_prompt = "You are an AI assistant helping write a kids book"
    response = queryLLM(query=prompt, system_prompt=system_prompt, client=client)
    return response

def getLost(name):
    lost_text = f"""From the medallion, one by one,
These animals, shining like the sun!
{name} gasped, eyes open wide,
So much to learn with friends beside.

But as they twirled in joyful cheer,
A thought crept in… a hint of fear.
The trees stood tall, the path was gone,
{name} was lost, and something was wrong"""
    return lost_text

def getEnding(name, story_so_far):
    prompt = f"""I need you to write the ending to a kids book. The book is about {name} who is learning about their cultral heritage through magical animals. They are now lost in a 
scary forest and need to get home. I want the animals to help them get home using the values they have taught {name}. Some of these values may seem not helpful for escaping a scary forest,
in these instances, feel free to add some new characters or encounters to make these values more applicable. Do you best to make sure each animal provides equal assistance to {name}. 
This final section of the story should be a 16-20 lines long. I will end this message with the story so far, please copy it's writing style.Only respond with the final section of the story, 
provide no other infomation or plesantries. Do not repeat the story you have already been sent. The story so far: {story_so_far}"""
    system_prompt = "You are an AI assistant helping write a kids book"
    response = queryLLM(query=prompt, system_prompt=system_prompt, client=client)
    return response