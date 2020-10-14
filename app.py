import warnings
warnings.filterwarnings('ignore')
import streamlit as st
import numpy as np
from PIL import Image
import os
import cv2
from keras.models import load_model
#from win32com.client import Dispatch

page_bg_img = '''
<style>
body {
background-image: url("https://www.uh.edu/class/comd/asli/_images/feature/170523-signs-of-success.jpg");
background-size: cover;

}
</style>
'''

st.markdown(page_bg_img, unsafe_allow_html=True)


#def speak(text):
    #speak = Dispatch(("SAPI.SpVoice"))
    #speak.Speak(text)
model = load_model('newasl.h5')

def preprocessing(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.resize(img, (100,100))
    return img

def main():
    html_temp = """
        <div style = "background-color: #195094; padding: 10px;">
            <center><h1>ASL Recognition using Deep Learning</h1></center>
        </div><br>
    """
    st.markdown(html_temp, unsafe_allow_html=True)

    #st.title("ASL Recognition using Deep Learning")
    st.set_option('deprecation.showfileUploaderEncoding', False)
    activities=["Classification","About"]
    choices = st.sidebar.selectbox("Select Activities",activities)

    if choices == "Classification":
        st.subheader("Predict the hand sign")
        img_file= st.file_uploader("Upload your Image",type=['png','jpg','jpeg'])
        if img_file is not None:
            up_img=Image.open(img_file)
            st.image(up_img)
        if st.button("Process"):
            img = np.asarray(up_img)
            img=cv2.resize(img,(100,100))
            img=preprocessing(img)
            img=img.reshape(1,100,100,1)
            prediction=model.predict(img)
            classIndex = model.predict_classes(img)
            probabilityValue=np.amax(prediction)
            if probabilityValue>0.90:
                if classIndex == 0:
                    st.success("A")
                    #speak("Predicted sign is A")
                elif classIndex == 1:
                    st.success("B")
                    #speak("Predicted sign is B")
                elif classIndex == 2:
                    st.success("C")
                    #speak("Predicted sign is C")
        #except Exception as e:
            #st.error("Please Try Again :(")

    elif choices=="About":

        st.write("American Sign Language (ASL) is the primary language used by many deaf individuals in North America, and it is also used by hard-of-hearing and hearing individuals. The language is as rich as spoken languages and employs signs made with the hand, along with facial gestures and bodily postures.In this project, we have used convolutional neural network to classify images of ASL.")

if __name__=='__main__':
    main()
