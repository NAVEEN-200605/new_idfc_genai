import time

def start_timer():
    return time.time()

def end_timer(start):
    return round(time.time() - start, 2)

def estimate_cost(num_images=1):
    # Hackathon-safe dummy estimate
    return round(num_images * 0.002, 4)
