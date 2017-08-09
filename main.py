import connect as cnt
import info_state as infs
import time

def main():
    infs.set_state()
    while True:
        infs.update_state()
        infs.set_state()
        time.sleep(0.1)

if __name__ == '__main__':
    main()