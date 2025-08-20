import os
import sys
import time
from src import commandline
from src import config
from src import bot
from src import logger


def acquire_lock():
    """Acquire a file lock to prevent multiple instances from running simultaneously"""
    lock_file = "posting.lock"
    try:
        lock_fd = os.open(lock_file, os.O_CREAT | os.O_EXCL | os.O_RDWR)
        with os.fdopen(lock_fd, 'w') as f:
            f.write(str(os.getpid()))
        return lock_file
    except OSError:
        # Lock file exists, check if process is still running
        if os.path.exists(lock_file):
            try:
                with open(lock_file, 'r') as f:
                    pid = int(f.read().strip())
                # Check if process is still running (Unix/Linux way)
                try:
                    os.kill(pid, 0)
                    print(f"Another instance is already running (PID: {pid})")
                    sys.exit(1)
                except (OSError, ProcessLookupError):
                    # Process is dead, remove stale lock file
                    os.remove(lock_file)
                    return acquire_lock()
            except (ValueError, IOError):
                # Invalid lock file, remove it
                os.remove(lock_file)
                return acquire_lock()
        return None

def release_lock(lock_file):
    """Release the file lock"""
    if lock_file and os.path.exists(lock_file):
        try:
            os.remove(lock_file)
        except OSError:
            pass

def check_for_unresolved_error(error_counter, response, edge):
    # Try 10 times before terminating the script
    if error_counter >= 10:
        print("Error still unresolved after 10 tries, bot exiting")
        logger.log_error(f"Unresolved error at {edge}, bot exiting")
        sys.exit(1)

    # Log the error response only once to prevent spamming in the log file
    if error_counter == 1:
        print(response)
        logger.log_error(response)

    # Wait 10 seconds before trying again
    print("Trying again after 10 seconds")
    logger.log_error("Trying again after 10 seconds")
    time.sleep(10)


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
    except IOError as e:
        print(f"Warning: Could not save progress: {e}")

def clear_progress():
    """Clear the progress file when all frames are completed"""
    progress_file = "posting_progress.txt"
    try:
        if os.path.exists(progress_file):
            os.remove(progress_file)
            print("Progress file cleared - all frames completed!")
    except IOError as e:
        print(f"Warning: Could not clear progress file: {e}")

def main():
    lock_file = None
    try:
        # Acquire lock to prevent multiple instances
        lock_file = acquire_lock()
        if lock_file is None:
            print("Could not acquire lock. Another instance may be running.")
            sys.exit(1)
        
        print("Lock acquired. Starting frame posting...")
        
        # Parse arguments from commandline
        commandline.process_arguments()

        # Store all the frames from the directory in a list in alphabetically sorted order
        # It is because the frame-number i isn't taken from the filename, rather it's the i-th file in the directory
        # Caution: Do not keep any other file or sub-directory in the directory except the frames
        pframes = sorted(os.listdir(config.pdir))
        cframes = []
        if config.cdir:
            cframes = sorted(os.listdir(config.cdir))

        total_frames = len(pframes)
        
        # Load progress to resume from where we left off
        frames_already_posted = load_progress()
        print(f"Resuming from frame #{frames_already_posted + 1} (already posted {frames_already_posted} frames)")
        
        # Adjust start position based on progress
        actual_start = config.start + frames_already_posted
        end = config.start + config.count  # Loop is run in [start, end) range, so +1 isn't necessary

        counter = frames_already_posted + 1 # counter for the number of frames posted

        # Loop body. Each iteration does four tasks related to a single frame
        # Namely, post, comment, add post-photo in album, add comment-photo in album
        for curren_frame in range(actual_start, end):

            # Only base filenames without the directory parts are stored in the list
            # Base-filenames must be joined back with their directory part
            pimage_basename = pframes[curren_frame - 1]  # Get the (i-1)th file from the list (0 based)
            pimage = f"{config.pdir}/{pimage_basename}"  # filename = directory/ + basename
            if config.cdir:
                cimage_basename = cframes[curren_frame - 1]
                cimage = f"{config.cdir}/{cimage_basename}"
            else:
                cimage = ""

            # Initialize the bot with variables for this loop
            bot.initialize(curren_frame, total_frames, pimage, cimage)

            comment_id = ""
            palbum_id = ""
            calbum_id = ""

            # Ask the bot to make the post
            post_response = bot.make_post()
            error_counter = 0
            while "post_id" not in post_response.keys():
                error_counter += 1
                check_for_unresolved_error(error_counter, post_response, "/page-id/photos")
                post_response = bot.make_post()

            post_id = post_response["post_id"]  # Get the post-id from json response
            print(f"---> Main post done")
            if config.verbose:
                print(f"Post response: {post_response}")

            if config.cdir:
                # Ask the bot to comment under the post
                comment_response = bot.make_comment(post_id)
                error_counter = 0
                while "id" not in comment_response.keys():
                    error_counter += 1
                    check_for_unresolved_error(error_counter, comment_response, "/post-id/comments")
                    comment_response = bot.make_comment(post_id)

                comment_id = comment_response["id"]  # Get the comment-id from json response
                print(f"---> Comment done")
                if config.verbose:
                    print(f"Comment response: {comment_response}")

            if config.palbum_id:
                # Ask the bot to add the photo-frame in album
                palbum_response = bot.make_album_post(post_id, config.palbum_id, "p")
                error_counter = 0
                while "post_id" not in palbum_response.keys():
                    error_counter += 1
                    check_for_unresolved_error(error_counter, palbum_response, "/palbum-id/photos")
                    palbum_response = bot.make_album_post(post_id, config.palbum_id, "p")

                palbum_id = palbum_response["post_id"]  # Get the photo-album-post-id from json response
                print(f"---> Album post done (Main)")
                if config.verbose:
                    print(f"Post-album response: {palbum_response}")

            if config.calbum_id:
                # Ask the bot to add the comment-frame in album
                calbum_response = bot.make_album_post(comment_id, config.calbum_id, "c")
                error_counter = 0
                while "post_id" not in calbum_response.keys():
                    error_counter += 1
                    check_for_unresolved_error(error_counter, calbum_response, "/calbum-id/photos")
                    calbum_response = bot.make_album_post(comment_id, config.calbum_id, "c")

                calbum_id = calbum_response["post_id"]  # Get the comment-album-post-id from json response
                print(f"---> Album post done (Comment)")
                if config.verbose:
                    print(f"Comment-album response: {calbum_response}")

            # Log the id's of the posts
            logger.log_posts(curren_frame, post_id, comment_id, palbum_id, calbum_id)

            time_12 = time.strftime("%I:%M:%S %p") # Get 12-hour clock time with AM/PM
            # time_locale = time.strftime("%x") # Get locale time

            print(f"{counter}. Done posting frame-number {curren_frame} - Time: {time_12}\n")

            # Save progress after each successful frame posting
            save_progress(counter)

            counter += 1
            
            # Always wait between frames to prevent simultaneous posting, except for the very last frame
            if curren_frame < end - 1:  # Not the last frame
                if config.verbose:
                    print(f"Waiting {config.delay} seconds before next frame...")
                time.sleep(config.delay)
            else:
                print("Last frame completed - no delay needed")

        # Clear progress file when all frames are completed
        print(f"Successfully posted all {config.count} frames!")
        clear_progress()

    except Exception as e:
        print(f"Error: {e}")
        logger.log_error(str(e))
        sys.exit(1)
    
    finally:
        # Always release the lock
        if lock_file:
            release_lock(lock_file)
            print("Lock released.")


if __name__ == '__main__':
    main()