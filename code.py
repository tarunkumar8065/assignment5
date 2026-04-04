class Process:
    def __init__(self, pid, at, bt, priority=0):
        self.pid = pid
        self.at = at
        self.bt = bt
        self.priority = priority
        self.ct = 0
        self.wt = 0
        self.tat = 0


# ---------------- FCFS ----------------
def fcfs(processes):
    processes.sort(key=lambda x: x.at)
    time = 0
    gantt = []

    for p in processes:
        if time < p.at:
            time = p.at
        gantt.append((p.pid, time))
        time += p.bt
        p.ct = time
        p.tat = p.ct - p.at
        p.wt = p.tat - p.bt

    return processes, gantt


# ---------------- SJF Non-Preemptive ----------------
def sjf_non_preemptive(processes):
    time = 0
    completed = []
    ready = []
    processes.sort(key=lambda x: x.at)
    n = len(processes)
    i = 0
    gantt = []

    while len(completed) < n:
        while i < n and processes[i].at <= time:
            ready.append(processes[i])
            i += 1

        if ready:
            ready.sort(key=lambda x: x.bt)
            p = ready.pop(0)
            gantt.append((p.pid, time))
            time += p.bt
            p.ct = time
            p.tat = p.ct - p.at
            p.wt = p.tat - p.bt
            completed.append(p)
        else:
            time += 1

    return completed, gantt


# ---------------- SJF Preemptive ----------------
def sjf_preemptive(processes):
    time = 0
    n = len(processes)
    remaining_bt = {p.pid: p.bt for p in processes}
    completed = 0
    gantt = []
    last = -1

    while completed < n:
        ready = [p for p in processes if p.at <= time and remaining_bt[p.pid] > 0]

        if ready:
            p = min(ready, key=lambda x: remaining_bt[x.pid])

            if last != p.pid:
                gantt.append((p.pid, time))
                last = p.pid

            remaining_bt[p.pid] -= 1
            time += 1

            if remaining_bt[p.pid] == 0:
                p.ct = time
                p.tat = p.ct - p.at
                p.wt = p.tat - p.bt
                completed += 1
        else:
            time += 1

    return processes, gantt


# ---------------- Priority (Non-Preemptive) ----------------
def priority_scheduling(processes):
    time = 0
    completed = []
    ready = []
    processes.sort(key=lambda x: x.at)
    n = len(processes)
    i = 0
    gantt = []

    while len(completed) < n:
        while i < n and processes[i].at <= time:
            ready.append(processes[i])
            i += 1

        if ready:
            ready.sort(key=lambda x: x.priority)
            p = ready.pop(0)
            gantt.append((p.pid, time))
            time += p.bt
            p.ct = time
            p.tat = p.ct - p.at
            p.wt = p.tat - p.bt
            completed.append(p)
        else:
            time += 1

    return completed, gantt


# ---------------- Round Robin ----------------
def round_robin(processes, tq):
    from collections import deque

    time = 0
    queue = deque()
    processes.sort(key=lambda x: x.at)
    remaining_bt = {p.pid: p.bt for p in processes}
    n = len(processes)
    i = 0
    gantt = []

    while queue or i < n:
        if not queue:
            time = max(time, processes[i].at)

        while i < n and processes[i].at <= time:
            queue.append(processes[i])
            i += 1

        p = queue.popleft()
        gantt.append((p.pid, time))

        exec_time = min(tq, remaining_bt[p.pid])
        time += exec_time
        remaining_bt[p.pid] -= exec_time

        while i < n and processes[i].at <= time:
            queue.append(processes[i])
            i += 1

        if remaining_bt[p.pid] > 0:
            queue.append(p)
        else:
            p.ct = time
            p.tat = p.ct - p.at
            p.wt = p.tat - p.bt

    return processes, gantt


# ---------------- Utility ----------------
def print_results(processes):
    print("\nPID AT BT CT TAT WT")
    for p in processes:
        print(p.pid, p.at, p.bt, p.ct, p.tat, p.wt)

    avg_wt = sum(p.wt for p in processes) / len(processes)
    avg_tat = sum(p.tat for p in processes) / len(processes)

    print("Average WT:", round(avg_wt, 2))
    print("Average TAT:", round(avg_tat, 2))


def print_gantt(gantt):
    print("\nGantt Chart:")
    for p, t in gantt:
        print(f"| P{p} ", end="")
    print("|")


# ---------------- Main ----------------
def main():
    n = int(input("Enter number of processes: "))
    processes = []

    for i in range(n):
        at = int(input(f"P{i+1} Arrival Time: "))
        bt = int(input(f"P{i+1} Burst Time: "))
        pr = int(input(f"P{i+1} Priority: "))
        processes.append(Process(i+1, at, bt, pr))

    while True:
        print("\n1.FCFS 2.SJF(NP) 3.SJF(P) 4.Priority 5.RoundRobin 6.Exit")
        choice = int(input("Enter choice: "))

        import copy
        proc_copy = copy.deepcopy(processes)

        if choice == 1:
            res, gantt = fcfs(proc_copy)
        elif choice == 2:
            res, gantt = sjf_non_preemptive(proc_copy)
        elif choice == 3:
            res, gantt = sjf_preemptive(proc_copy)
        elif choice == 4:
            res, gantt = priority_scheduling(proc_copy)
        elif choice == 5:
            tq = int(input("Enter Time Quantum: "))
            res, gantt = round_robin(proc_copy, tq)
        else:
            break

        print_results(res)
        print_gantt(gantt)


if __name__ == "__main__":
    main()
