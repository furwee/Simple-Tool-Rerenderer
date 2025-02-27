class Stack:
    def __init__(self, list2stack):
        if list2stack is None:
            self.list2stack = []
        else:
            self.list2stack = [].append(list2stack)
        self.last = len(self.list2stack) - 1

    def push(self, item=None):
        if self.last <= 32:
            self.list2stack.append(item)
            self.last += 1
        else:
            self.dequeue()
            self.list2stack.append(item)
        # print(self.last)

    def pop(self):
        self.list2stack = self.list2stack[:self.last-1]

    def dequeue(self):
        self.list2stack = self.list2stack.remove(0)

    def getCurrent(self):
        return self.list2stack[self.last]

    def undo(self):
        if self.last > 0:
            self.last -= 1
            self.last = self.last
        else:
            self.last = self.last
        print(self.last)
        return self.getCurrent()

    def redo(self):
        # print(self.list2stack)
        if self.last < len(self.list2stack) - 1:
            self.last += 1
            self.last = self.last
        else:
            self.last = self.last
        print(self.last)
        return self.getCurrent()

    def getSize(self):
        return len(self.list2stack)


def main():
    pass


main()

if __name__ == "__main__": main()
