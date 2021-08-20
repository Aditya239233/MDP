import time
import _thread

class PathPlanner:
    def __init__(self):
        self.data = []
        self.cache = {}
        self.job_id = 0
        self.counter = 0
    
    def say(self):
        print("I am in PathPlanner")
    
    def add_job(self, data):
        self.counter += 1
        self.job_id += 1
        self.data.append(data)
        return self.job_id
        
    def get_id(self):
        return self.job_id

    def start(self):
        while True:
            if(self.counter != 0):
                self.do_job(self.job_id) 
            else:
                time.sleep(5)

    def do_job(self, job_id):
        self.counter -= 1
        print("Doing job ", job_id)
        time.sleep(5)
        self.cache[job_id] = [(1,2,3), (4,5,6)]

    def get_cache(self, job_id):
        job_id = int(job_id)
        if job_id not in self.cache:
            return None
        else:
            return self.cache[job_id]

    def get_arena(self):
        return self.data[0]