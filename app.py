from detect import *
import streamlit as st
from PIL import Image
from datetime import datetime
import random


def get_detection_folder(path='./runs/detect'):
    '''
        Returns the latest folder in a runs\detect
    '''
    result = []
    for d in os.listdir(path):
        bd = os.path.join(path, d)
        if os.path.isdir(bd):
            result.append(bd)
    return max(result, key=os.path.getmtime)

@st.cache
def get_audio_bytes(music):
    audio_file = open(f'data/music/{music}-周杰伦.mp3', 'rb')
    audio_bytes = audio_file.read()
    audio_file.close()
    return audio_bytes

@st.experimental_singleton
def get_video_bytes(video):
    video_file = open(video, 'rb')
    video_bytes1 = video_file.read()
    video_file.close()
    return video_bytes1

opt = parse_opt()

#  http://share.streamlit.io/

#-----------------------------title---------------------------
st.set_page_config(
    page_title="yolov5",    #页面标题
    page_icon=":rainbow:",        #icon
    layout="wide",                #页面布局
    initial_sidebar_state="auto"  #侧边栏
)
st.title('yolov5:heart:')

#-----------------------------日期---------------------------
st.session_state.date_time=datetime.now() 
d=st.sidebar.date_input('Date',st.session_state.date_time.date())
st.sidebar.write(f'The current date is {d}')

#-----------------------------音乐---------------------------
music=st.sidebar.radio('Select Music You Like',['七里香','稻香'],index=random.choice(range(2)))
st.sidebar.write(f'正在播放 {music}-周杰伦 :musical_note:')
audio_bytes=get_audio_bytes(music)
st.sidebar.audio(audio_bytes, format='audio/mp3')


#-----------------------------yolo5检测---------------------------
source = st.sidebar.radio('数据类型',('图片','视频'))
is_valid=False

if source=='图片':
    st.write('**图片检测**')    
    uploaded_file = st.sidebar.file_uploader("上传图片", type=['png', 'jpeg', 'jpg'])
    if uploaded_file is not None:
        is_valid = True
        with st.spinner(text='资源加载中...'):
            st.sidebar.image(uploaded_file)
            picture = Image.open(uploaded_file)
            picture = picture.save(f'data/images/{uploaded_file.name}')
            opt.source = f'data/images/{uploaded_file.name}'
else:
    st.write('视频检测')
    uploaded_file = st.sidebar.file_uploader("上传视频", type=['mp4'])
    if uploaded_file is not None:
        is_valid = True
        with st.spinner(text='资源加载中...'):
            st.sidebar.video(uploaded_file)
            with open(os.path.join("data", "videos", uploaded_file.name), "wb") as f:
                f.write(uploaded_file.getbuffer())
            opt.source = f'data/videos/{uploaded_file.name}'

if is_valid:
    print('valid')
    if st.button('开始检测'):
        main(opt)
        if source== '图片':
            with st.spinner(text='Preparing Images'):
                for img in os.listdir(get_detection_folder()):
                    st.image(str(Path(f'{get_detection_folder()}') / img))

                st.balloons()
        else:
            with st.spinner(text='Preparing Video'):
                for vid in os.listdir(get_detection_folder()):
                    
                    #st.video(str(Path(f'{get_detection_folder()}') / vid))
                    st.video(get_video_bytes(os.path.join(get_detection_folder(), vid)))

                st.balloons()


