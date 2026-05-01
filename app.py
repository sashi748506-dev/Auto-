import streamlit as st
import subprocess
import os
import zipfile
from io import BytesIO

st.set_page_config(page_title="Bulk Video Remixer", page_icon="🎬")

st.title("🎬 Batch Video Remixer (Max 10-15 Videos)")
st.write("Videos upload karein aur system unhe 'Slowed + Reverb' mein convert kar dega.")

# Bulk upload handle karne ke liye
uploaded_files = st.file_uploader("Videos select karein", type=['mp4', 'mov', 'avi'], accept_multiple_files=True)

if uploaded_files:
    st.info(f"{len(uploaded_files)} videos taiyar hain.")
    
    if st.button("Processing Shuru Karein"):
        output_files = []
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Output folder create karein
        if not os.path.exists("output"):
            os.makedirs("output")

        for i, uploaded_file in enumerate(uploaded_files):
            # Progress update
            progress = (i + 1) / len(uploaded_files)
            progress_bar.progress(progress)
            status_text.text(f"Processing: {uploaded_file.name} ({i+1}/{len(uploaded_files)})")

            # Temp files handle karein
            input_fn = f"in_{uploaded_file.name}"
            output_fn = f"output/remix_{uploaded_file.name}"
            
            with open(input_fn, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # FFmpeg Command
            v_filters = "hflip,scale=1.1*iw:-1,crop=iw/1.1:ih/1.1,setpts=1.1*PTS,eq=saturation=1.3:contrast=1.1"
            a_filters = "atempo=0.9,asetrate=44100*0.9,aresample=44100,aecho=0.8:0.88:60:0.4"
            
            cmd = [
                'ffmpeg', '-i', input_fn,
                '-vf', v_filters, '-af', a_filters,
                '-c:v', 'libx264', '-crf', '24', '-preset', 'ultrafast',
                '-c:a', 'aac', '-b:a', '128k',
                output_fn, '-y'
            ]
            
            try:
                subprocess.run(cmd, check=True)
                output_files.append(output_fn)
                os.remove(input_fn) # Memory bachane ke liye input delete karein
            except Exception as e:
                st.error(f"Error in {uploaded_file.name}: {e}")

        # ZIP file banakar download ka option dein
        if output_files:
            zip_buffer = BytesIO()
            with zipfile.ZipFile(zip_buffer, "w") as zf:
                for f in output_files:
                    zf.write(f, os.path.basename(f))
                    os.remove(f) # Server space saaf karein
            
            st.success("✅ Batch Complete!")
            st.download_button(
                label="Edited Videos (ZIP) Download Karein",
                data=zip_buffer.getvalue(),
                file_name="batch_remixed.zip",
                mime="application/zip"
            )
            
