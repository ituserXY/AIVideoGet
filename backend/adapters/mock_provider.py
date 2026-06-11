import random
from .base import ParseResult

# Sample video data for testing
MOCK_VIDEOS = {
    "douyin": [
        ParseResult(
            title="【4K】绝美风景航拍合集",
            author="摄影师小王",
            cover_url="https://picsum.photos/seed/douyin1/640/360",
            video_url="https://test-videos.co.uk/vids/bigbuckbunny/mp4/h264/720/Big_Buck_Bunny_720_10s_1MB.mp4",
            duration=15,
            width=720,
            height=1280,
            file_size=5_000_000,
        ),
        ParseResult(
            title="今天教你做一道拿手菜 #美食 #教程",
            author="美食日记",
            cover_url="https://picsum.photos/seed/douyin2/640/360",
            video_url="https://test-videos.co.uk/vids/bigbuckbunny/mp4/h264/720/Big_Buck_Bunny_720_10s_1MB.mp4",
            duration=42,
            width=720,
            height=1280,
            file_size=12_000_000,
        ),
    ],
    "kuaishou": [
        ParseResult(
            title="农村生活记录：今天的收获",
            author="乡村小张",
            cover_url="https://picsum.photos/seed/kuaishou1/640/360",
            video_url="https://test-videos.co.uk/vids/bigbuckbunny/mp4/h264/720/Big_Buck_Bunny_720_10s_1MB.mp4",
            duration=30,
            width=720,
            height=1280,
            file_size=8_000_000,
        ),
    ],
    "xiaohongshu": [
        ParseResult(
            title="周末探店｜这家咖啡店太出片了",
            author="探店达人",
            cover_url="https://picsum.photos/seed/xhs1/640/360",
            video_url="https://test-videos.co.uk/vids/bigbuckbunny/mp4/h264/720/Big_Buck_Bunny_720_10s_1MB.mp4",
            duration=25,
            width=720,
            height=1280,
            file_size=6_000_000,
            images=["https://picsum.photos/seed/xhs_img1/640/800", "https://picsum.photos/seed/xhs_img2/640/800"],
        ),
    ],
    "bilibili": [
        ParseResult(
            title="【干货】如何搭建自己的网站？从零开始全教程",
            author="技术宅小林",
            cover_url="https://picsum.photos/seed/bili1/640/360",
            video_url="https://test-videos.co.uk/vids/bigbuckbunny/mp4/h264/720/Big_Buck_Bunny_720_10s_1MB.mp4",
            duration=360,
            width=1920,
            height=1080,
            file_size=50_000_000,
        ),
    ],
    "weibo": [
        ParseResult(
            title="热搜现场：城市夜景灯光秀",
            author="新闻快报",
            cover_url="https://picsum.photos/seed/weibo1/640/360",
            video_url="https://test-videos.co.uk/vids/bigbuckbunny/mp4/h264/720/Big_Buck_Bunny_720_10s_1MB.mp4",
            duration=20,
            width=720,
            height=1280,
            file_size=4_000_000,
        ),
    ],
    "xigua": [
        ParseResult(
            title="纪录片：深海探秘全记录",
            author="探索频道",
            cover_url="https://picsum.photos/seed/xigua1/640/360",
            video_url="https://test-videos.co.uk/vids/bigbuckbunny/mp4/h264/720/Big_Buck_Bunny_720_10s_1MB.mp4",
            duration=180,
            width=1920,
            height=1080,
            file_size=80_000_000,
        ),
    ],
}


def get_mock_result(platform: str, url: str) -> ParseResult:
    """Get mock parse result for testing purposes."""
    videos = MOCK_VIDEOS.get(platform, MOCK_VIDEOS["douyin"])
    result = random.choice(videos)
    # Keep the original URL for tracking
    return ParseResult(
        title=result.title,
        author=result.author,
        cover_url=result.cover_url,
        video_url=result.video_url,
        duration=result.duration,
        width=result.width,
        height=result.height,
        images=result.images,
        file_size=result.file_size,
    )
