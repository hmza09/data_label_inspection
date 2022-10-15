import json
import time
import random
import urllib
import  streamlit as st
from datetime import datetime, date
from pages.instructions import tutorial
import streamlit.components.v1 as components
from pages.demographic_form import demo, user_input_check
from pages.thankyou import task_complete
from pages.task import open_image
from pages.func import isvalid, blob_upload, max_already, session_data, page_label
from pages.obstacle import header_example

st.set_page_config(
     page_title="Data Label Crowdsourcing",
     page_icon="🧊",
     layout="wide",
     initial_sidebar_state="expanded",
 )
hide_streamlit_style = """
                <style>
                #MainMenu {
                visibility: hidden;
                height: 0%;
                }
                header {
                visibility: hidden;
                height: 0%;
                }
                footer {
                visibility: hidden;
                height: 0%;
                }
                </style>
                """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

query_params = st.experimental_get_query_params()
if 'worker_id' in query_params.keys():
    worker_id = query_params['worker_id'][0]
    worker_id = worker_id.replace('{','')
    worker_id = worker_id.replace('}','')
    st.session_state.worker_id = worker_id


if 'campaign_id' in query_params.keys():
    campaign_id =  query_params['campaign_id'][0]
    campaign_id = campaign_id.replace('{','')
    campaign_id = campaign_id.replace('}','')
    st.session_state.campaign_id = campaign_id

st.session_state.SECRET_KEY = 'QhwnRHYB0BIwJOER'

########################### USER SESSION #####################################
#from streamlit.report_thread import get_report_ctx
#def _get_session():
#    import streamlit.report_thread as ReportThread
#    from streamlit.server.server import Server
#    session_id = get_report_ctx().session_id
#    session_info = Server.get_current()._get_session_info(session_id)
#    if session_info is None:
#        raise RuntimeError("Couldn't get your Streamlit Session object.")
#    return session_info.session
#st.session_state.user_session = user_session = _get_session()
##############################################################################

input_dir = "./pages/"
root_dir = st.session_state.root_dir = ""
data_jso = st.session_state.root_dir + "/traindata.json"

st.session_state.MAX_WORKERS = 40
sessions_user = root_dir + '/sessions_task03.json'

now = datetime.now()
st.session_state.start_time = now.strftime("%H:%M:%S")
st.session_state.start_date = date.today()


if isvalid(sessions_user):
    with urllib.request.urlopen(sessions_user) as file:
        dataset  = json.load(file)
    if worker_id == "DummyWorkerId" and "DummyWorkerId" in dataset.keys():
        st.session_state.choose = "dummy_task"
    if not worker_id in dataset:
        dataset[worker_id] = {'page_status' : 7, 'start_date' : st.session_state.start_date, 'start_time': st.session_state.start_time, 'campaign_id': st.session_state.campaign_id}
        blob_upload(container_name="crowdsourcing-data", file_name='sessions_task03.json', data=dataset)
else:
    workers = {}
    status = {}
    status['page_status'] = 7
    status['start_date'] = st.session_state.start_date
    status['start_time'] = st.session_state.start_time
    status['campaign_id'] = st.session_state.campaign_id
    workers[st.session_state.worker_id] = status
    blob_upload(container_name="crowdsourcing-data", file_name='sessions_task03.json', data=workers)
    dataset = workers







### Choice of Page to be displayed
if "choose" in  st.session_state:
    choose = st.session_state.choose
    #st.write(choose)
else:
    choose = max_already(dataset)
    if choose == None:
        choose = st.session_state.choose = "instructions"
        st.session_state.page_status = 7

### Choice of object class to be displayed
if "object" in st.session_state:
    object = st.session_state.object
    #st.write(object)
else:
    with urllib.request.urlopen(data_jso) as file:
        dataset  = json.load(file)
    object_list = list(dataset.keys())
    object = st.session_state.object = random.choice(object_list)

#st.write(st.session_state)
def forward_choice():
    if not "demo" in st.session_state:
        sess_data = session_data()
        choose = max_already(sess_data=sess_data)
        if choose == None:
            st.session_state.choose = "demo"
            st.session_state.page_status = 6
            sess_data[worker_id]['page_status'] = 6
            blob_upload(container_name="crowdsourcing-data", file_name='sessions_task03.json', data=sess_data)
    else:
        sess_data = session_data()
        choose = max_already(sess_data=sess_data)
        if choose == None:
            st.session_state.choose = "task"
            st.session_state.page_status = 5
            sess_data[worker_id]['page_status'] = 5
            blob_upload(container_name="crowdsourcing-data", file_name='sessions_task03.json', data=sess_data)

def backward_choice():
    st.session_state.choose = "instructions"


def task_choice():
    sess_data = session_data()
    choose = max_already(sess_data=sess_data)
    if choose == None:
        st.session_state.choose = "task"
        st.session_state.page_status = 5
        sess_data[worker_id]['page_status'] = 5
        blob_upload(container_name="crowdsourcing-data", file_name='sessions_task03.json', data=sess_data)


def task():
    #st.write("task page")
    st.button("Back", on_click= backward_choice)


if choose == "instructions":
    HtmlFile = open("pages/header.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read() 
    components.html(source_code, height=220, scrolling=True)
    st.image(page_label('intro_label.png'))
    header_example(st.session_state.object)
    tutorial(object=st.session_state.object)
    #st.write(st.session_state.page_status)
    if "first_time" in st.session_state:
        st.button("Next", on_click=forward_choice)
    else:
        st.session_state.first_time = True
        with st.empty():
            for seconds in range(29):
                st.write(f"⏳ {30 - seconds} to go to Next Page")
                time.sleep(1)
            st.write("✔️ 1 minute over!")
            st.button("Next",on_click=forward_choice)
elif choose == "demo":
    demo()
    if user_input_check() == True:
        st.session_state.demo = True
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.button("Previous",on_click=backward_choice)
        with col3:
            st.button("Next",on_click=task_choice)
elif choose == "task":
    open_image(object=st.session_state.object)
elif choose == "thank_you":
    task_complete()
elif choose == "max_reached":
    st.title("Oops! Sorry maximum number of feedbacks reached already.")
elif choose == "already_finished":
    st.title("Oops! Sorry you  have already finished the task!")
elif choose == "dummy_task":
    st.title("Please Modify WORKER_ID")
st.markdown('##')
st.markdown('##')
st.markdown('<a href="mailto:hamzashafiqde@gmail.com">Contact us !</a>', unsafe_allow_html=True)