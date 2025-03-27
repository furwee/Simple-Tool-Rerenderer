import os


class Stack:
    def __init__(self, list2stack):
        if list2stack is None:
            self.list2stack = []
        else:
            self.list2stack = [].append(list2stack)
        self.last = len(self.list2stack) - 1

    def push(self, item=None):
        if self.last < 8:
            self.list2stack.append(item)
            self.last += 1
        else:
            state = self.popS()
            self.last -= 1 if state is False else True
            self.list2stack.append(item)
        print(self.list2stack)

    def getCurrent(self):
        return self.list2stack[self.last]

    def undo(self):
        if self.last > 0:
            self.last -= 1
            self.last = self.last
        else:
            self.last = self.last
        # print(self.last)
        return self.getCurrent()

    def redo(self):
        # print(self.list2stack)
        if self.last < len(self.list2stack) - 1:
            self.last += 1
            self.last = self.last
        else:
            self.last = self.last
        # print(self.last)
        return self.getCurrent()

    def getSize(self):
        return len(self.list2stack)

    def popS(self):
        getCur = self.list2stack[0]
        print(getCur)
        self.list2stack.pop(0)
        if os.path.exists(getCur[1][0]):
            os.remove(getCur[1][0])
            return True
        else:
            os.remove(self.list2stack[1][1][0])
            return False

def main():
    pass


main()

if __name__ == "__main__": main()
