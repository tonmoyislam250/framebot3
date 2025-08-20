#!/usr/bin/env python3
"""
Simple test script to verify progress tracking functionality
"""
import os

def load_progress():
    """Load the progress from a file, return the number of frames already posted"""
    progress_file = "posting_progress.txt"
    if os.path.exists(progress_file):
        try:
            with open(progress_file, 'r') as f:
                return int(f.read().strip())
        except (ValueError, IOError):
            return 0
    return 0

def save_progress(frames_posted):
    """Save the current progress to a file"""
    progress_file = "posting_progress.txt"
    try:
        with open(progress_file, 'w') as f:
            f.write(str(frames_posted))
        print(f"Progress saved: {frames_posted} frames posted")
    except IOError as e:
        print(f"Warning: Could not save progress: {e}")

def clear_progress():
    """Clear the progress file when all frames are completed"""
    progress_file = "posting_progress.txt"
    try:
        if os.path.exists(progress_file):
            os.remove(progress_file)
            print("Progress file cleared!")
    except IOError as e:
        print(f"Warning: Could not clear progress file: {e}")

if __name__ == "__main__":
    print("Testing progress tracking...")
    
    # Test initial state
    print(f"Initial progress: {load_progress()}")
    
    # Test saving progress
    save_progress(50)
    print(f"After saving 50: {load_progress()}")
    
    # Test saving more progress
    save_progress(100)
    print(f"After saving 100: {load_progress()}")
    
    # Test clearing progress
    clear_progress()
    print(f"After clearing: {load_progress()}")
    
    print("Progress tracking test completed!")
