import json
from datetime import datetime

def generate_report(elapsed_seconds, params, accuracy, user_genre, recommended_genre, logs, best):
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report = {
        'elapsed': f"{elapsed_seconds:.2f}s",
        "params": params,
        "accuracy": accuracy,
        "user_genre": user_genre,
        "recommended_genre": recommended_genre,
        "logs": logs,
        "best": best
        
    }
    
    with open(f"reports/{current_time}_report.json", "w") as json_file:
        json.dump(report, json_file, indent=4)
    
    return f"Report saved as {current_time}_report.json"

def calculate_genre_accuracy(user_genre_count, best_recommended_genre_count):
    accuracy = {}
    
    user_total = user_genre_count["sum"]
    
    for genre in user_genre_count:
        if genre != "sum":
            user_count = user_genre_count[genre]
            recommended_count = best_recommended_genre_count.get(genre, 0)
            
            margin = 0.90

            recommended_total = recommended_count * margin
            
            if user_count >= recommended_count:
                genre_accuracy = 100.0
            else:
                genre_accuracy = (user_count / (user_count + recommended_total)) * 100
            
            accuracy[genre] = f"{genre_accuracy:.2f}%"
    
    return accuracy

def calculate_global_accuracy(accuracy):
    genre_accuracies = [float(acc.strip('%')) for acc in accuracy.values()]
    global_accuracy = sum(genre_accuracies) / len(genre_accuracies)
    return f"Total Accuracy: {global_accuracy:.2f}%"