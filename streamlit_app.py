import streamlit as st
import random 
# from pkg.src.src import (
#     generate_plan, 
# )

st.set_page_config(
   page_title="blog-content-generation",
   page_icon="🧊",
   layout="wide",
   initial_sidebar_state="expanded",
)

def generate_plan(input) -> list[str] : 
    return [input + str(i) for i in range(5)]

def generate_title(input) -> str: 
    return input

def generate_intro() :
    pass

def generate_outro() : 
    pass

def publish_article() : 
    pass

def article_layout() :
    pass

def gen_random_key() -> int :
    return random.randint(0,1000000)

if __name__ == "__main__" : 

    # if "article_dic" not in st.session_state : 
    #     print("Entry init dic")
    #     # st.session_state["article_dic"] = {"search_intent":""}
    #     st.session_state["article_dic"] = {"search_intent":"",

    #                         "title":"",
    #                         "plan":[],
    #                         "guidance":"",
    #                         "intro":"",
    #                         "outro":"",
    #                         "paragraphs":[],

    #                         "stable_prompt":"",
    #                         "img_title":"",
    #                         "jpg_name":"",
    #                         "img_alt":"",

    #                         "nearest_title":"",
    #                         "nearest_title_CTA":"",
    #                         "backlink_slug":"",
                            
    #                         "book_title":"",
    #                         "book_CTA":"",
    #                         "book_link":"",
    #                         "book_description":"",

    #                         "bold_list":[],

    #                         "yt_id":"",
    #                         "yt_title":"",
    #                         "yt_url":"",

    #                         "slug":"",
    #                         }

    with st.sidebar : 
        st.text_input("OpenAI API key", key="openai_api_key", help="https://help.openai.com/en/articles/4936850-where-do-i-find-my-openai-api-key")
        st.text_input(label="Language to generate", key="language", help="Desired output language for text generation")
        st.text_input(label="WordPress API Key", key="wp_api_key")

    st.text_input("Search Intent eg. 'How to grow carrots ?'", key="search_intent", help="The target search intent you want the article to address. Ideally formulated as a question. Can also take precisions to orient the plan generation on specific angles.")

    if st.button("Generate Plan") :
        # st.session_state["article_dic"]["search_intent"] = search_intent
        temp_input = st.session_state["search_intent"]
        st.session_state["title"] = generate_title(temp_input)
        st.session_state["plan"] = generate_plan(temp_input)
        st.session_state["intro"] = generate_intro()
        st.session_state["outro"] = generate_outro()
        st.session_state["paragraphs"] = [""]*len(st.session_state["plan"])
        print("Session state : ", st.session_state)
        st.divider()

    st.text_input(label="Introduction", value="Introduction", key="intro_title")
    st.text_area(label="a", value=st.session_state["intro"], label_visibility="collapsed", key="intro")

    st.divider()

    for (idx, header), paragraph in zip(enumerate(st.session_state["plan"]), st.session_state["paragraphs"]) : 
        st.text_input(f"Header {idx}", value = header, key=f"header{idx}")
        st.text_area(label = "a", value=paragraph, label_visibility="collapsed", key=f"par{idx}")
        st.divider()

    st.text_input(label="Conclusion", value="Conclusion", key="outro_title")
    st.text_area(label = "a", value=st.session_state["outro"], label_visibility="collapsed", key="outro")


    draft = st.toggle("Draft/Public", value=False)

    publish = st.button("Publish", on_click=publish_article)

    print(draft)

    # needed output dict : 

    # auto_post(output_dict, key)
