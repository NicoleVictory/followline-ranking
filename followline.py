def record_time(name, run, time):
    # Record the time of the competitor run
    with open("runs_log.txt", "a") as log_file:
        log_file.write(f"{name}: {run}: {time}\n")

    # Update the ranking and write it to a file
    ranking = get_ranking()
    with open("ranking.txt", "w") as ranking_file:
        ranking_file.write("Ranking:\n")
        for i, (name, time) in enumerate(ranking):
            if time == '':
                ranking_file.write(f"{i+1}. {name}: Falhou em completar todas as tentativas\n")
            elif time == 'fail':
                ranking_file.write(f"{i+1}. {name}: Não completou uma das tentativas\n")
            else:
                ranking_file.write(f"{i+1}. {name}: {time:.2f}\n")

def get_ranking():
    # Get the ranking of competitors based on their best time.
    
    with open("runs_log.txt") as log_file:
        lines = log_file.readlines()
   
    ranking = {}
    for line in lines:
        
        name, run, time = line.strip().split(": ")
        # If this is the first time we've seen this competitor, initialize their times to infinity
        if name not in ranking:
            ranking[name] = [float('inf'), float('inf'), float('inf')]
        # If the competitor completed the run and their time is faster than their previous best time for this run, update their time
        if time != 'fail' and time != '':
            try:
                time = float(time)
            except ValueError:
                time = float('inf')
            if time < ranking[name][int(run)-1]:
                ranking[name][int(run)-1] = time
        else:
            # If the competitor didn't complete the run, record it as "fail" or an empty string
            ranking[name][int(run)-1] = '' if time == '' else 'fail'
    # Create a list of tuples (name, best time), where best time is the minimum of the competitor's three times
    result = []
    for name, runs in ranking.items():
        valid_runs = [t for t in runs if t != '' and t != 'fail']
        if len(valid_runs) == 0:
            best_time = float('inf')
        else:
            best_time = min(valid_runs)
        result.append((name, best_time))
    # Sort the list by best time (or by infinity if the competitor didn't complete any runs)
    return sorted(result, key=lambda x: x[1] if isinstance(x[1], float) else float('inf'))


    
num_competitors = int(input("Insira o número de equipes: "))
# This code considers that each competitor has 3 chances/runs
# For each competitor, ask for their name and their times for each of the three runs
for i in range(num_competitors):
    name = input(f"\nInsira o nome da {i+1}° equipe: ")
    for j in range(1, 4):
        while True:
            time = input(f"Insira o tempo da {j}° tentativa (ou 'fail' se o competidor não completou a pista): ")
            if time == 'fail' or time == '':
                record_time(name, j, time)
                break
            try:
                time = float(time)
                record_time(name, j, time)
                break
            except ValueError:
                print("Entrada inválida. Tente novamente.")
