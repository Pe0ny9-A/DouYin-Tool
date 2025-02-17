import argparse
import main

def parse_arguments():
    parser = argparse.ArgumentParser(description="抖音数据分析工具")
    parser.add_argument("video_id", type=str, help="视频ID")
    return parser.parse_args()

def run_app():
    args = parse_arguments()
    main.video_id = args.video_id
    main.main()

if __name__ == "__main__":
    run_app()
