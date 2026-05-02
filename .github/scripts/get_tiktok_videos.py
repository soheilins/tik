import asyncio
import csv
import os
from TikTokApi import TikTokApi

async def get_recent_videos(username: str, num_videos: int = 20):
    video_urls = []
    async with TikTokApi() as api:
        # Pass the username of the TikTok user you want to fetch videos from
        user = api.user(username=username)
        
        # This will fetch the user's videos. The number fetched might be more than requested.
        # The script will then trim down to the exact number needed.
        video_count = 0
        async for video in user.videos():
            if video_count >= num_videos:
                break
            # Construct the standard TikTok video URL
            video_url = f"https://www.tiktok.com/@{username}/video/{video.id}"
            video_urls.append(video_url)
            video_count += 1

    return video_urls

async def main():
    # Get the TikTok username from GitHub Actions environment variable
    tiktok_username = os.getenv('TIKTOK_USERNAME')
    if not tiktok_username:
        print("Error: TIKTOK_USERNAME environment variable not set.")
        return

    print(f"Fetching videos for user: @{tiktok_username}")
    
    # Fetch the video URLs
    urls = await get_recent_videos(tiktok_username)
    
    # Define the output file name
    output_file = "recent_video_links.txt"
    
    # Write the URLs to a text file
    with open(output_file, 'w') as f:
        for url in urls:
            f.write(f"{url}\n")
    
    print(f"Successfully wrote {len(urls)} URLs to {output_file}")

if __name__ == "__main__":
    asyncio.run(main())
