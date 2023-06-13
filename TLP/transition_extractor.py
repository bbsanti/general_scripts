import pandas as pd 
from tkinter import Tk
from tkinter.filedialog import askdirectory
from os import path, makedirs, system
from pathlib import Path
import os
from scenedetect import open_video, SceneManager, AdaptiveDetector

# csv_file = 'J:/MLB_Downloads/YES_NYY@TBR/YES_NYY@TBR-Scenes.csv'
# csv_file_2 = csv_file.replace(".csv","_2.csv")
# video_file = 'J:/MLB_Downloads/YES_NYY@TBR/YES_NYY@TBR.mp4'
# video_filename = 'YES_NYY@TBR'
# # # with open('', 'r') as file:
# # #     # Read and print each line in the file
# # #     for line in file:
# # #         print(line.strip())

# with open(csv_file,'r') as f:
#     with open(csv_file_2,'w+') as f1:
#         next(f) # skip header line
#         for line in f:
#             f1.write(line)


# df = pd.read_csv(csv_file_2)
# frame_list = list(df["Start Time (seconds)"])

# for i in range(len(frame_list)):
#     if frame_list[i] >  5:
#         frame_list[i] = frame_list[i] - 5
#     else:
#         pass
        

# for i in frame_list:
#     v = i+10
#     print(f'extracting @ {i}')
#     os.system(f'cmd /c ffmpeg -y -i {video_file} -ss {i} -to {v} -codec copy {video_filename}_{i}.mp4')

# # subprocess.call(['ffmpeg', '-i', video_file, '-vf',f"select=gte(n\,{i})" , '-t', '5', f'{video_file}_{i}.mp4'])

# #file_list = []
# cuts_folder = '{}'.format(askdirectory(title='Folder of Cuts CSVs',mustexist=True))
# #filedir = Path(filedir)
# videos_folder = '{}'.format(askdirectory(title='Folder where replays are',mustexist=True))

# export_folder = '{}'.format(askdirectory(title='Folder to place exported clips',mustexist=True))

# for filename in os.listdir(cuts_folder):
#     file_path = os.path.join(cuts_folder, filename)
#     # Check if the file is a regular file (not a folder)
#     if os.path.isfile(file_path):
#         cut_name = os.path.basename(file_path)
#         cut_name = os.path.splitext(cut_name)[0]
#         folder_check = os.path.join(export_folder,cut_name)
#         if not os.path.exists(folder_check):
#             os.mkdir(folder_check)    
#         else:
#             exit()


root = Tk()
root.wm_attributes('-topmost',1)
root.after_idle(root.attributes,'-topmost',False)
root.withdraw()

cuts_list= []
cut_name = ''
filename_noext = ''
cuts_path = ''
export_path = ''
file_path = ''
extensions = ['.mp4','.mov','.mkv','.avi']

# videos_folder = '{}'.format(askdirectory(title='Folder where replays are',mustexist=True))
# cuts_folder = '{}'.format(askdirectory(title='Folder of Cuts CSVs',mustexist=True))
# export_folder = '{}'.format(askdirectory(title='Folder to place exported clips',mustexist=True))

videos_folder = 'J:/MLB_Downloads'
cuts_folder = 'J:/MLB_Downloads/2023_mlb_cuts'
export_folder = 'D:/MLB_Clips_Exports'

def make_csv_and_clips_created ():
    global cuts_list, cuts_folder, videos_folder, export_folder,cut_name, filename_noext, cuts_path, export_path, file_path, extensions

    for filename in os.listdir(videos_folder):
        
        print (videos_folder,cuts_folder,export_folder)

        file_path = os.path.join(videos_folder, filename)
        # Check if the file is a regular file (not a folder)
        if file_path.endswith(tuple(extensions)):
            filename_noext = os.path.splitext(filename)[0]
            cuts_path = os.path.join(cuts_folder, filename_noext+'.csv')
            export_path = os.path.join(export_folder, filename_noext)

        if not os.path.exists(cuts_path):
            detect_cuts()
            make_clips()
        elif os.path.exists(cuts_path) and not os.path.exists(export_path):
            make_clips()
        elif os.path.exists(export_path):
            print(f"{filename_noext} is already clipped")
        else:
             raise Exception("what happened?")
    print("Done!")


def detect_cuts():
    print(f'finding cuts in {filename_noext}')
    os.system(f'cmd /c scenedetect -o {cuts_folder} -i {file_path} detect-adaptive list-scenes --skip-cuts --filename {filename_noext}.csv')

def make_clips():
    df = pd.read_csv(cuts_path)
    frame_list = list(df["Start Time (seconds)"])
    #end_list = list(df["End Time (seconds)"])

    for i in range(len(frame_list)):
        back_time = 6
        forward_time = 3
        frame_pos = frame_list[i] 
        #end_list[i] = end_list[i] + forward_time

        if  frame_pos >  back_time:
            frame_pos = frame_pos - back_time
        else:
            pass

    os.mkdir(export_path)

    #for i,v in zip(frame_list,end_list):
    for i in frame_list:
        v = i+12
        print(f'clipping {filename_noext} @ {i}')
        os.system(f'cmd /c ffmpeg -y -i {file_path} -ss {i} -to {v} -codec copy {export_path}/{filename_noext}_{i}.mp4')

make_csv_and_clips_created ()

    # for i in cuts_list:
    #     cut_name = os.path.basename(i)
    #     cut_name = os.path.splitext(cut_name)[0]
    #     folder_check = os.path.join(export_folder,cut_name)
    #     if not os.path.exists(folder_check):
    #         os.mkdir(folder_check)

    #     else:
    #         pass


