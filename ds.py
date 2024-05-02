import heapq
from collections import deque

# Linked List
class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None


# Stack
class Stack:
    def __init__(self):
        self.stack = []

    def push(self, item):
        self.stack.append(item)

    def pop(self):
        if len(self.stack) < 1:
            return None
        return self.stack.pop()


# Queue
queue = deque()

# Tree
class Node:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key


# Heap
heap = []
heapq.heapify(heap)

# Graph
graph = {
    "A": ["B", "C"],
    "B": ["A", "D", "E"],
    "C": ["A", "F"],
    "D": ["B"],
    "E": ["B", "F"],
    "F": ["C", "E"],
}

# Hash Map
class HashMap:
    def __init__(self):
        self.size = 10000
        self.buckets = [[] for _ in range(self.size)]

    def hash(self, key):
        return hash(key) % self.size

    def put(self, key, value):
        hash_key = self.hash(key)
        key_exists = False
        bucket = self.buckets[hash_key]
        for i, kv in enumerate(bucket):
            k, v = kv
            if key == k:
                key_exists = True
                break
        if key_exists:
            bucket[i] = (key, value)
        else:
            bucket.append((key, value))

    def get(self, key):
        hash_key = self.hash(key)
        bucket = self.buckets[hash_key]
        for i, kv in enumerate(bucket):
            k, v = kv
            if key == k:
                return v
        return None
