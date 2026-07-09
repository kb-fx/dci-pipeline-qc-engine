import subprocess
import json

def get_media_metadata(file_path):
    # The command array that Python will execute in the background
    command = [
        'ffprobe', 
        '-v', 'error', 
        '-show_entries', 'stream=avg_frame_rate,channels', 
        '-show_entries', 'format=bit_rate', 
        '-of', 'json', # Forces FFprobe to output clean, structured data
        file_path
    ]
    
    # Run the system command and capture the text output
    result = subprocess.run(command, capture_output=True, text=True)
    
    # Parse the string text into a Python dictionary
    metadata = json.loads(result.stdout)
    return metadata


# --- MAIN AUTOMATION EXECUTION ---
if __name__ == "__main__":
    # Point this at your VIDEO .mxf file this time!
    target_file = "D:\\PROJECTS\\FILM_MASTERING_PROJECT\\04_DELIVERABLES\\Test_DCP\\TestDcp_FTR-1_F-190_XX-XX_MOS_2K_20260703_SMPTE_OV\\j2c_f4446c23-3d53-4a26-976a-c61ebd544cf7.mxf"
    
    print("Initializing Media Pipeline Quality Control Check...")
    
    try:
        # 1. Get the raw data dictionary
        data = get_media_metadata(target_file)
        
        # 2. Extract specific variables safely from the JSON dictionary
        # We use .get() so the script doesn't crash if the data is missing
        bitrate_str = data.get('format', {}).get('bit_rate', '0')
        streams = data.get('streams', [])
        
        # Grab channel count (defaulting to 0 if no channels exist)
        channels = streams[0].get('channels', 0) if len(streams) > 0 else 0
        
        # 3. Math Conversions
        # FFprobe returns bitrate in pure bits. We need Megabits (Mbps).
        bitrate_bps = int(bitrate_str)
        bitrate_mbps = bitrate_bps / 1000000 
        
        # -----------------------------------------
        # 4. THE ENGINEERING LOGIC (COMPLIANCE RULES)
        # -----------------------------------------
        print("\n========================================")
        print("      DCI COMPLIANCE REPORT CACHE       ")
        print("========================================\n")

        # RULE A: Audio Matrix Validation
        if channels >= 6:
            print(f"[PASS] Audio Matrix : {channels} channels detected. Layout is DCI compliant.")
        else:
            print(f"[FAIL] Audio Matrix : Only {channels} channels detected! Theater servers require 6 or 8.")

        # RULE B: Video Bitrate Ceiling Validation
        if bitrate_mbps <= 250:
            print(f"[PASS] Bandwidth    : {bitrate_mbps:.2f} Mbps (Safe beneath 250 Mbps limit).")
        else:
            print(f"[FAIL] Bandwidth    : {bitrate_mbps:.2f} Mbps EXCEEDS THEATRICAL LIMITS! Server crash imminent.")
            
        print("\n========================================")

    except Exception as e:
        print(f"[SYSTEM ERROR]: Failed to parse media file. Details: {e}")