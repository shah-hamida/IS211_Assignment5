from collections import deque


class Request:

    def __init__(self, second,filename, processtime):
        self.second = second
        self.filename = filename.strip()
        self.processtime = processtime

    def getsecond(self):
        return self.second

    def getprocesstime(self):
        return self.processtime

class Server:
    def __init__(self):
        self.currentTask = None
        self.timeRemaining = 0

    def tick(self):
        if self.currentTask:
            self.timeRemaining -= 1
            if self.timeRemaining <= 0:
                self.currentTask = None

    def busy(self):
        return self.currentTask

    def nextRequest (self, new_request):
        self.currentTask = new_request
        self.timeRemaining = new_request.getprocesstime()

def simulationOneServer(filename):
    requests = []

    with open(filename, 'r') as file:
        for line in file:
            time, filename, processtime = line.strip().split(',')
            requests.append(Request(time,filename, processtime))

    server = Server()
    queue = deque()
    waitingSecond = []

    currentSeconds = 0
    requestsnum = 0

    while requestsnum < len(requests) or queue or server.busy():
        while (requestsnum < len(requests) and
               requests[requestsnum].getsecond() == currentSeconds):
                queue.append(requests[requestsnum])
                requestsnum += 1


        if(not server.busy()) and queue:
            nextRequest = queue
            waitingSecond.append(currentSeconds - nextRequest.getsecond())
            server.nextRequest(nextRequest)

    server.tick()
    currentSeconds +=1


    average = sum(waitingSecond) / len(waitingSecond)
    print(f"Average wait time = {average}")
    return average

def main():
    simulationOneServer('requests.csv')


if __name__ == "__main__":
    """Main entry point"""
    main()
