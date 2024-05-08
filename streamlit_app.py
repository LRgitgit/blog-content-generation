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
    st.session_state["title"] = generate_title(st.session_state["search_intent"])
    generate_plan_parts(st.session_state["search_intent"])

def generate_plan_parts(_input) : 
     for idx in range(5) : 
          st.session_state[f"header{idx}"] = _input + str(idx)

def generate_title(input) -> str: 
    return "Title : " + input

def generate_intro() :
    st.session_state["intro"] = "This is intro"

def generate_outro() : 
    st.session_state["outro"] = "This is outro"

def publish_article() : 
    pass

def article_layout() :
    pass


if __name__ == "__main__" : 

    #Init of dynamic elements
    if "intro" not in st.session_state : 
            st.session_state["intro"] = ""
    
    if "outro" not in st.session_state : 
            st.session_state["outro"] = ""

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

    col1, col2, col3 = st.columns(3, gap="small")
    with col1 : 
        gen_plan = st.button("Generate Plan")
        
    with col2 : 
         gen_xtros = st.button("Generate intro and outro")
    
    with col3 : 
         gen_plan_parts = st.button("Generate plan parts")
    
    st.divider()

    if gen_plan : 
        generate_plan(st.session_state["search_intent"])
    
    if gen_xtros : 
        generate_intro()
        generate_outro()

    if gen_plan_parts : 
         generate_plan_parts()

    st.text_input(label="Introduction", value="Introduction", key="intro_title")
    st.text_area(label="a", value=st.session_state["intro"], label_visibility="collapsed", key="intro")

    st.divider()

    for idx in range(sum([1 for i in st.session_state if "header" in i])) : 
        st.text_input(f"Header {idx}", key=f"header{idx}")
        st.text_area(label = "a", label_visibility="collapsed", key=f"par{idx}")
        st.divider()

    st.text_input(label="Conclusion", value="Conclusion", key="outro_title")
    st.text_area(label = "a", value=st.session_state["outro"], label_visibility="collapsed", key="outro")


    draft = st.toggle("Draft/Public", value=False)

    publish = st.button("Publish", on_click=publish_article)

    # print(draft)

    [print(k, st.session_state[k]) for k in sorted(st.session_state)]

    # needed output dict : 

    # auto_post(output_dict, key)
