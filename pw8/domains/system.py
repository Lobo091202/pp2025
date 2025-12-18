import os
import pickle
import zlib
import threading
import queue
import time

from .student import Student
from .course import Course

DATA_DIR = "data"
DATA_PATH = os.path.join(DATA_DIR, "system.dat")

class BackgroundSaver(threading.Thread):
    def __init__(self, system_obj, path=DATA_PATH):
        super().__init__(daemon=False)
        self._system_obj = system_obj
        self._path = path
        self._q = queue.Queue()
        self._stop_event = threading.Event()
        # keep simple lock not to conflict with system lock (system provides lock)
        # uses system_obj._lock when pickling

    def run(self):
        while not self._stop_event.is_set():
            try:
                item = self._q.get(timeout=0.5)
            except queue.Empty:
                continue

            if item == "save":
                try:
                    self._do_save()
                except Exception as e:
                    print("Background save error:", e)
                finally:
                    self._q.task_done()
            elif item == "stop":
                # drain and process remaining save requests then stop
                while not self._q.empty():
                    try:
                        it = self._q.get_nowait()
                        if it == "save":
                            try:
                                self._do_save()
                            except Exception as e:
                                print("Background save error during draining:", e)
                            finally:
                                self._q.task_done()
                    except queue.Empty:
                        break
                self._q.task_done()
                break

    def request_save(self):
        # enqueue a save request (non-blocking)
        self._q.put("save")

    def stop(self, wait=True):
        # enqueue stop signal and optionally wait for finish
        self._q.put("stop")
        if wait:
            self.join(timeout=30)

    def _do_save(self):
        # acquire system lock (system provides it) to get consistent state
        # system_obj implements get_state_for_pickle()
        state = None
        # Ask system for state safely
        state = self._system_obj.get_state_for_pickle()
        raw = pickle.dumps(state)
        compressed = zlib.compress(raw)

        os.makedirs(os.path.dirname(self._path), exist_ok=True)
        tmp_path = self._path + ".tmp"
        with open(tmp_path, "wb") as f:
            f.write(compressed)
        os.replace(tmp_path, self._path)


class StudentMarkSystem:
    def __init__(self):
        self.students = []      # list of Student objects
        self.courses = []       # list of Course objects
        self.credit_dict = {}   # course_id -> credit

        # runtime-only attributes (not pickled)
        self._saver = None
        self._lock = threading.RLock()  # protect state during get_state_for_pickle or modifications

    # ---------- helpers ----------
    def find_student(self, sid):
        for s in self.students:
            if s.get_id() == sid:
                return s
        return None

    def find_course(self, cid):
        for c in self.courses:
            if c.get_id() == cid:
                return c
        return None

    # ---------- add data ----------
    def add_student(self, sid, name, dob):
        with self._lock:
            if self.find_student(sid):
                raise ValueError(f"Student id {sid} already exists")
            self.students.append(Student(sid, name, dob))

    def add_course(self, cid, name, credit):
        with self._lock:
            if self.find_course(cid):
                raise ValueError(f"Course id {cid} already exists")
            self.courses.append(Course(cid, name, credit))
            self.credit_dict[cid] = credit

    def input_marks_for_course(self, cid):
        if self.find_course(cid) is None:
            raise ValueError(f"Course {cid} not found")
        # input_mark modifies student internal marks; we hold lock while calling to avoid race with saver
        with self._lock:
            for s in self.students:
                s.input_mark(cid)

    # ---------- GPA ----------
    def calculate_all_gpa(self):
        with self._lock:
            for s in self.students:
                s.calculate_gpa(self.credit_dict)

    def sort_students_by_gpa_desc(self):
        with self._lock:
            self.students.sort(key=lambda x: x.get_gpa() if x.get_gpa() is not None else 0.0, reverse=True)

    # ---------- state extraction for pickling ----------
    def get_state_for_pickle(self):
        # Return a plain dict of data to be pickled.
        # Acquire lock to ensure consistent snapshot.
        with self._lock:
            # students and courses are objects; we will pickle them directly (classes are defined)
            # It's acceptable because student/course classes are picklable.
            return {
                "students": self.students,
                "courses": self.courses,
                "credit_dict": self.credit_dict
            }

    @staticmethod
    def build_from_state(state):
        obj = StudentMarkSystem()
        with obj._lock:
            obj.students = state.get("students", [])
            obj.courses = state.get("courses", [])
            obj.credit_dict = state.get("credit_dict", {})
        return obj

    # ---------- background saver API ----------
    def start_background_saver(self, path=DATA_PATH):
        if self._saver is not None:
            return
        self._saver = BackgroundSaver(self, path)
        self._saver.start()

    def request_save(self):
        # if saver present, enqueue, otherwise do sync save
        if self._saver is not None:
            self._saver.request_save()
            return None
        else:
            return self.save_data_sync()

    def stop_background_saver(self, wait=True):
        if self._saver is not None:
            self._saver.stop(wait=wait)
            self._saver = None

    # ---------- synchronous save/load (used as fallback) ----------
    def save_data_sync(self, path=DATA_PATH):
        state = self.get_state_for_pickle()
        raw = pickle.dumps(state)
        compressed = zlib.compress(raw)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        tmp_path = path + ".tmp"
        with open(tmp_path, "wb") as f:
            f.write(compressed)
        os.replace(tmp_path, path)
        return path

    @staticmethod
    def load_data(path=DATA_PATH):
        if not os.path.exists(path):
            return None
        with open(path, "rb") as f:
            compressed = f.read()
        raw = zlib.decompress(compressed)
        state = pickle.loads(raw)
        return StudentMarkSystem.build_from_state(state)
