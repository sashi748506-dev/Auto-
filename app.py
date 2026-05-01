import streamlit as st
import subprocess
import os

st.set_page_config(page_title="AI Video Remixer", page_icon="🎬")

st.title("🎬 Professional Video Remixer")
st.write("Apni video upload karein aur 'Slowed + Reverb' version turant payein.")

uploaded_file = st.file_uploader("Video select karein (mp4, mov, avi)", type=['mp4', 'mov', 'avi'])

if uploaded_file is not None:
    # Save uploaded file
    with open("temp_input.mp4", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.video("temp_input.mp4")
    
    if st.button("Magic Edit Shuru Karein"):
        with st.spinner('Processing ho rahi hai... Isme thoda waqt lag sakta hai.'):
            output_file = "remixed_video.mp4"
            
            # Aapka FFmpeg Logic
            v_filters = "hflip,scale=1.1*iw:-1,crop=iw/1.1:ih/1.1,setpts=1.1*PTS,eq=saturation=1.3:contrast=1.1"
            a_filters = "atempo=0.9,asetrate=44100*0.9,aresample=44100,aecho=0.8:0.88:60:0.4"
            
            cmd = [
                'ffmpeg', '-i', 'temp_input.mp4',
                '-vf', v_filters,
                '-af', a_filters,
                '-c:v', 'libx264', '-crf', '22', '-preset', 'veryfast',
                '-c:a', 'aac', '-b:a', '128k',
                output_file, '-y'
            ]
            
            try:
                subprocess.run(cmd, check=True)
                st.success("Video Taiyar Hai!")
                
                # Download Button
                with open(output_file, "rb") as file:
                    st.download_button(
                        label="Edited Video Download Karein",
                        data=file,
                        file_name="remixed_video.mp4",
                        mime="video/mp4"
                    )
            except Exception as e:
                st.error(f"Kuch galat hua: {e}")
              
