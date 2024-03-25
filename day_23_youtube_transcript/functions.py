from langchain_community.document_loaders import YoutubeLoader


def get_transcription_from_yt_video(video_url):
    # Transcribe the videos to text
    loader = YoutubeLoader.from_youtube_url(
        video_url, add_video_info=False
    )
    docs = loader.load()

    # Combine doc
    combined_docs = [doc.page_content for doc in docs]
    text = " ".join(combined_docs)

    return text
