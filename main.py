from functions import audio, reddit, video, directories, upload, openai
import os

def main():
    number_of_posts = 3  # number of posts created (3 stories per day in a video)
    posts = reddit.from_reddit_to_posts(number_of_posts)  # gets the best posts

    week_directory_path = directories.weekly_directory()

    print("Do you want to upload? (y/n)")
    answer = input()

    for t in range(number_of_posts // 3):  # create each post
        # crea cartella per posts
        directory_path = directories.daily_directory(t + 1, week_directory_path)
        print(directory_path)
        video_paths = []
        video_title = "ERROR"
        video_description = "ERROR"
        short_title = "ERROR"
        short_description = "ERROR"
        link_to_full_video = "ERROR"
        link_to_short_video = "ERROR"
        for i in range(3):

            # video_title e video_description con chatGPT (da fare) (al posto delle successive due righe)
            body = posts.iloc[t * 3].loc["body"]
            video_title, video_description = openai.title_description(body)

            voice = openai.gender(body)

            if i == 0:
                short_title = video_title + " short"
                # MODIFICARE SHORT_DESCRIPTION PER INSERIRE IL LINK DEL VIDEO COMPLETO
                short_description = video_description + " #short"

            if i == 2:
                lista_str_and_dur = audio.from_post_to_audio(posts.iloc[t * 3 + i], voice, True)  # create a file audio
            else:
                lista_str_and_dur = audio.from_post_to_audio(posts.iloc[t * 3 + i], voice)

            video_paths.append(video.from_audio_to_video(directory_path, lista_str_and_dur, video_title, t * 3 + i))  # create story video

        full_video_path = video.video_merge(video_paths, directory_path, video_title)

        if answer == "y":

            link_to_full_video = upload.upload_video(full_video_path, video_title, video_description, t+1)
            print("Full video link:", link_to_full_video)

        # crea short

        short_description = f"You can watch the full video by subscribing to the channel and by this link:\n{link_to_full_video}\n" + short_description
        short_path = video.creaShort(video_paths[0], directory_path, short_title)

        if answer == "y":

            link_to_short_video = upload.upload_video(short_path, short_title, short_description, t+1)

        if link_to_short_video != "ERROR":
            print(f"Everything should have been uploaded for day {t+1}")
        else:
            print(f"Error for upload {t+1}")

        print(f"video title: {video_title}")
        print(f"video description: {video_description}")
        print(f"short title: {short_title}")
        print(f"short description: {short_description}")

        # Elimina i video originali
        for percorso in video_paths:
            os.remove(percorso)
    """
    for i in range(number_of_posts):
        video_title = posts.iloc[i].loc["title"][:15]
        video_path = f"./output/{i}, {video_title}.mp4"
        if st.getDuration(video_path) >= 60:
            st.creaShort(video_path,i)
    """


if __name__ == "__main__":
    main()
