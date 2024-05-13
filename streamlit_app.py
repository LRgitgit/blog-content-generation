import streamlit as st
from streamlit_tags import st_tags #https://github.com/gagan3012/streamlit-tags/tree/master

import random 
from openai import OpenAI

from secret import get_openai_api_key

#Params to check for chat completion : 
#frequency_penalty and presence_penalty : Can help improve the lexical diversity of the answer by penalizing tokens repetitions. TBD if it hurts the information density
#logit bias : allow to push or prohibit the utilisation of given tokens in the answer. Can be used to invite to keywords utilisation

# from pkg.src.src import (
#     generate_plan, 
# )

st.set_page_config(
   page_title="blog-content-generation",
   page_icon="🧊",
   layout="wide",
   initial_sidebar_state="expanded",
)

def undo_action() : 
    # Method should work but bc of a multiple reloads (3) at each state change, try to consider the last one is not functioning
    # Idk from where it comes
    st.session_state = st.session_state["previous_state"]

def delete_paragraph(idx) : 
    idx_to_remove = st.session_state["headers_idx_order"].index(idx)
    st.session_state["headers_idx_order"].pop(idx_to_remove)

def generate_plan(input) -> list[str] : 
    generate_title(st.session_state["search_intent"])
    generate_plan_parts(st.session_state["search_intent"])


def generate_plan_parts(_input) : 
     # The 0 idx should be left free to allow add paragraph button to work in intro
    for idx in range(0, 5) : 
        st.session_state[f"header{idx}"] = _input + str(idx)
    st.session_state["headers_idx_order"] = list(range(0, 5))


def generate_title(input) -> str: 
    st.session_state["title"] = "This is the title"


def generate_intro() :
    st.session_state["intro"] = "This is intro"


def generate_outro() : 
    st.session_state["outro"] = "This is outro"


def generate_paragraphs() : 
     for idx, header in enumerate(sorted([i for i in st.session_state if "header" in i])) : 
          st.session_state[f"paragraph{idx}"] = f"This is paragraphs for plan part {idx}"


def modify_paragraph(idx) :
    print("Arguments : ", idx) 
    st.session_state[f"paragraph{idx}"] = st.session_state[f"prompt_modif_par{idx}"]


def modify_xtro(xtro) : 
    st.session_state[xtro] = st.session_state[f"prompt_modif_{xtro}"]


def get_keypoints() : 
    return ["option " + str(i) for i in range(5)]


def publish_article() : 
    pass

### App layout functions
def init_sidebar() : 
    st.text_input(label="Language to generate", key="language", help="Desired output language for text generation")
    st.selectbox(label="Model to use", options=["gpt-3.5-turbo-0125", "gpt-4-turbo"], index = 0, key="model")

    st.text_input("OpenAI API key", key="openai_api_key", help="https://help.openai.com/en/articles/4936850-where-do-i-find-my-openai-api-key")
    st.text_input(label="WordPress API Key", key="wp_api_key")

def init_gen_buttons() : 
    col1, col2, col3, col4 = st.columns(4, gap="small")
    with col1 : 
        gen_plan = st.button("Generate Plan")
    with col2 : 
        # The way to display key points is TBD, in par text_area or in different text_area to keep them when paragraph is generated
        gen_key_points = st.button("Generate content points")
        
    with col3 : 
        gen_paragraphs = st.button("Generate paragraphs")
    
    with col4 : 
        gen_xtros = st.button("Generate intro and outro")

    return gen_plan, gen_xtros, gen_key_points, gen_paragraphs

def init_title() : 
    if "title" in st.session_state : 
        with st.expander("Image to use") : 
            if "uploaded_files" in st.session_state : 
                st.selectbox(label="Image to use", options=[None] + [img.name for img in st.session_state["uploaded_files"]], key="img_title")
                st.text_input(label="Image description", key="img_title_description")
            else : 
                st.write("No uploaded image to use")

        st.text_area(label="Title", value=st.session_state["title"], key="title")

def init_intro() : 
    if "intro" in st.session_state : 
        with st.expander("Image to use") : 
            if "uploaded_files" in st.session_state : 
                st.selectbox(label="Image to use", options=[None] + [img.name for img in st.session_state["uploaded_files"]], key="img_intro")
                st.text_input(label="Image description", key="img_intro_description")
            else : 
                st.write("No uploaded image to use")

        st.text_input(label="Introduction", value="Introduction", key="intro_title")

        col_intro, col_buttons = st.columns(2)
        with col_intro : 
            st.text_area(label="a", value=st.session_state["intro"], label_visibility="hidden", key="intro")
            st.button("Add paragraph", on_click=add_paragraph, kwargs={"idx":-1}, key=f"add_par_button_{-1}")
        with col_buttons : 
            st.text_area(label="Modification instructions", key=f"prompt_modif_intro")
            st.button("Modify paragraph", on_click=modify_xtro, kwargs={"xtro":"intro"},key="modif_par_button_intro")

def init_outro() :
    if "outro" in st.session_state : 
        with st.expander("Image to use") : 
            if "uploaded_files" in st.session_state : 
                st.selectbox(label="Image to use", options=[None] + [img.name for img in st.session_state["uploaded_files"]], key=f"img_outro")
                st.text_input(label="Image description", key="img_outro_description")
            else : 
                st.write("No uploaded image to use")

        st.text_input(label="Conclusion", value="Conclusion", key="outro_title")
        col_outro, col_buttons = st.columns(2)
        with col_outro : 
            st.text_area(label="a", value=st.session_state["outro"], label_visibility="hidden", key="outro")
            
        with col_buttons : 
            st.text_area(label="Modification instructions", key=f"prompt_modif_outro")
            st.button("Modify paragraph", on_click=modify_xtro, kwargs={"xtro":"outro"}, key="modif_par_button_outro")

    with st.expander("Image to use") : 
        if "uploaded_files" in st.session_state : 
            st.text_input(label="Image to use", key="img_end")
            st.text_input(label="Image description", key="img_end_description")
        else : 
                st.write("No uploaded image to use")
    

def init_paragraphs() :
    # for idx in range(sum([1 for i in st.session_state if "header" in i])) : 
    for idx in st.session_state["headers_idx_order"] : 
        with st.expander("Image to use") :
            if "uploaded_files" in st.session_state :  
                st.selectbox(label="Image to use", options=[None] + [img.name for img in st.session_state["uploaded_files"]], key=f"img_par{idx}")
                st.text_input(label="Image description", key=f"img_par{idx}_description")
            else : 
                st.write("No uploaded image to use")

        st.text_input(f"Header {idx}", key=f"header{idx}")
        
        key_points_list = get_keypoints()
        # st_tags is bit buggy when a lot (~>10 are instanciated), causing some of them to not be charged and even sometimes be defined as None into st.session_state
        st_tags(label="Key points to adress", value=key_points_list, key=f"par{idx}_tags")
        
        col_text, col_buttons = st.columns(2)
        with col_text :
            st.text_area(label = "a", label_visibility="hidden", key=f"paragraph{idx}")
            st.button("Add paragraph", on_click=add_paragraph, kwargs={"idx":idx}, key=f"add_par_button_{idx}")
        with col_buttons : 
            st.text_area(label="Modification instructions", key=f"prompt_modif_par{idx}")
            st.button("Modify paragraph", on_click=modify_paragraph, kwargs={"idx":idx}, key=f"modif_par_button_{idx}")
        st.divider()

def add_paragraph(idx) :
    new_idx = max(st.session_state["headers_idx_order"]) + 1
    if idx >= 0 : 
        insert_idx = st.session_state["headers_idx_order"].index(idx)
        st.session_state["headers_idx_order"].insert(insert_idx + 1, new_idx)
    else : 
        # Account for the intro add paragraph button which have index -1, not very elegant yet functional for now
        st.session_state["headers_idx_order"].insert(0, new_idx)

@st.cache_resource
def init_open_ai_client() : 
    print('Init OPENAI client')
    client = OpenAI(organization='org-RodcoqHxocoaCNHWBLlJGpaX',
                    project='blog-content-gen-ui',
                    api_key = get_openai_api_key()
                   )
    return client 

@st.cache_data
def cache_images() : 
    return st.session_state["uploaded_files"]
    

if __name__ == "__main__" : 

    #Init of dynamic elements
    # if "intro" not in st.session_state : 
    #         st.session_state["intro"] = ""
    
    # if "outro" not in st.session_state : 
    #         st.session_state["outro"] = ""

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
    st.session_state["previous_state"] = st.session_state
    st.button("Undo", on_click=undo_action)
    client = init_open_ai_client()

    # Add an undo button that replace the current st.session_state with the stored previous one

    with st.sidebar : 
        init_sidebar()

    tab_modif, tab_preview, tab_advices, tab_upload = st.tabs(["Modifications", "Preview", "Writing advices", "Upload Images"])

    with tab_modif : 
        st.text_input("Search Intent eg. 'How to grow carrots ?'", key="search_intent", help="The target search intent you want the article to address. Ideally formulated as a question. Can also take precisions to orient the plan generation on specific angles.")
            
        gen_plan, gen_xtros, gen_key_points, gen_paragraphs = init_gen_buttons()
            
        st.divider()

        #Buttons click actions, could be replaced with on_click func to go further
        if gen_plan : 
            generate_plan(st.session_state["search_intent"])
        
        if gen_xtros : 
            generate_intro()
            generate_outro()

        if gen_paragraphs : 
            generate_paragraphs()

        init_title()

        st.divider()

        init_intro()

        st.divider()

        init_paragraphs()

        init_outro()

        st.divider()

        draft = st.toggle("Draft/Public", value=False)
        publish = st.button("Publish", on_click=publish_article)

        [print(k, st.session_state[k]) for k in sorted(st.session_state)]

    with tab_preview : 
        headers_keys = [key for key in sorted(st.session_state) if "header" in key]
        par_keys = [key for key in sorted(st.session_state) if "paragraph" in key]

        if "img_title" in st.session_state and st.session_state["img_title"] is not None : 
            st.image([obj for obj in st.session_state["uploaded_files"] if obj.name == st.session_state["img_title"]])

        st.markdown("# " + st.session_state["title"].replace("\n"," "))

        if "img_intro" in st.session_state and st.session_state["img_intro"] is not None : 
            st.image([obj for obj in st.session_state["uploaded_files"] if obj.name == st.session_state["img_intro"]])
        
        st.markdown("## " + st.session_state["intro_title"])
        st.markdown(st.session_state["intro"])

        for header_key, par_key in zip(headers_keys, par_keys) : 
            if f"img_{par_key}" in st.session_state and st.session_state[f"{par_key}"] is not None : 
                st.image([obj for obj in st.session_state["uploaded_files"] if obj.name == st.session_state[f"{par_key}"]])
            st.markdown("## " + st.session_state[header_key])
            st.markdown(st.session_state[par_key])

        if "img_outro" in st.session_state and st.session_state["img_outro"] is not None : 
            st.image([obj for obj in st.session_state["uploaded_files"] if obj.name == st.session_state["img_outro"]])

        st.markdown("## " + st.session_state["outro_title"])
        st.markdown(st.session_state["outro"])     

        if "img_end" in st.session_state and st.session_state["img_end"] is not None : 
            st.image([obj for obj in st.session_state["uploaded_files"] if obj.name == st.session_state["img_end"]])

    with tab_advices : 
        st.markdown("# Tab to display writing advices : \n * Keywords to use (per paragraph, with volumes ?) \n * Concurrents analysis : \n \t * Theme adressed by concurrents on subsequent topic/keywords \n \t * Themes not adressed by concurrent and that make original content \n * Possible angles to use for this topic \n * Images gathered around the theme, scraped and directly usable \n * Scraped sentences and/or paragraphs that answers the best for each paragraphs (even a posible small search engine on the vector DB once it's calculated)")

    with tab_upload : 
        st.file_uploader("Upload image", accept_multiple_files=True, key="uploaded_files")
        cache_images()
        st.write("Available files : ", [img.name for img in st.session_state["uploaded_files"]])

