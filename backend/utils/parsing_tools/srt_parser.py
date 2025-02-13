import srt
import os
from dotenv import load_dotenv

load_dotenv()

def format_timedelta(td):
    """Convert timedelta to HH:MM:SS format."""
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"

def parse_chunks(srt_file_name):
    """Parse an SRT file and return chunks of text every 16 subtitles."""
    with open(srt_file_name, 'r') as f:
        data = f.read()
        subtitles = list(srt.parse(data))  # Convert generator to list

        results = []
        content = ""
        start_time = None

        for s in subtitles:
            content += s.content
            if s.index % 16 == 0:
                if start_time is None:
                    start_time = s.start

                results.append({
                    "index": len(results) + 1,
                    "content": content,
                    "start_time": format_timedelta(start_time),
                    "end_time": format_timedelta(s.end),
                    "seconds": start_time.total_seconds()
                })

                # Update start_time for the next block
                start_time = s.end
                content = ""

        # If there's any remaining content after the loop
        if content:
            results.append({
                "index": len(results) + 1,
                "content": content,
                "start_time": format_timedelta(start_time) if start_time else None,
                "end_time": "-",
                "seconds": start_time.total_seconds() if start_time else None
            })
    
    return results

def get_srt_files(srt_dir):
    """Retrieve a list of SRT files from a directory."""
    return [os.path.join(srt_dir, file) for file in os.listdir(srt_dir) if file.endswith('.srt')]
