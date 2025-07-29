import pandas as pd

def tag_videos(df: pd.DataFrame) -> pd.DataFrame:
    def get_genre(desc, tags):
        desc = desc.lower()
        tags = [t.lower() for t in tags]
        if "minecraft" in desc or "minecraft" in tags:
            return "Gaming"
        elif "roblox" in desc or "roblox" in tags:
            return "Gaming"
        elif "animation" in desc or "animation" in tags:
            return "Animation"
        elif "music" in desc or "music" in tags:
            return "Music"
        return "Other"

    def get_animation_type(desc, tags):
        desc = desc.lower()
        tags = [t.lower() for t in tags]
        if "stopmotion" in desc or "stopmotion" in tags:
            return "Stopmotion"
        elif "3d" in desc or "3d" in tags:
            return "3D"
        elif "plot" in desc or "story" in desc:
            return "Plot"
        return "Other"

    def get_content_type(duration_str):
        # Shorts are less than 60 seconds
        import isodate
        try:
            duration = isodate.parse_duration(duration_str).total_seconds()
            return "Short" if duration < 60 else "Long"
        except Exception:
            return "Unknown"

    def has_copyright(desc, tags):
        # Placeholder: You may need to manually tag or use a list of known copyrighted terms
        copyright_terms = ["copyright", "licensed", "all rights reserved"]
        text = desc.lower() + " " + " ".join([t.lower() for t in tags])
        return any(term in text for term in copyright_terms)

    df["Genre"] = df.apply(lambda row: get_genre(row["description"], row["tags"]), axis=1)
    df["AnimationType"] = df.apply(lambda row: get_animation_type(row["description"], row["tags"]), axis=1)
    df["ContentType"] = df["duration"].apply(get_content_type)
    df["Copyrighted"] = df.apply(lambda row: has_copyright(row["description"], row["tags"]), axis=1)
    df["Year"] = pd.to_datetime(df["published"]).dt.year
    df["Month"] = pd.to_datetime(df["published"]).dt.month
    df["DayOfWeek"] = pd.to_datetime(df["published"]).dt.day_name()
    return df