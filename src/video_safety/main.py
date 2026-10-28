import subprocess
import sys
from video_safety.analyzer import analyze_video


def run_cli():
    url = sys.argv[2] if len(sys.argv) > 2 else "https://www.youtube.com/watch?v=aqz-KE-bpKQ"
    print(f"Auditing video: {url} ...")
    report = analyze_video(url)

    print(f"\nVerdict: {report.overall_verdict}")
    print(f"Safety Score: {report.safety_score} / 100")
    print(f"Summary: {report.summary}")

    print(f"\nViolations ({len(report.violations)}):")
    if report.violations:
        for v in report.violations:
            print(f"  - [{v.timestamp}] ({v.severity}) {v.category}: {v.description}")
    else:
        print("  None detected.")

    print(f"\nRecommended Edits:")
    if report.recommended_edits:
        for edit in report.recommended_edits:
            print(f"  - {edit}")
    else:
        print("  None required.")


def main():
    if "--cli" in sys.argv:
        run_cli()
    else:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "src/video_safety/app.py"])


if __name__ == "__main__":
    main()
