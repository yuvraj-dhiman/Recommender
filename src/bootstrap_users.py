import users
import numpy as np

def synthetic_user_prefs(num_users, num_clusters, num_topics, cluster_length, user_length):
    cluster_means = [np.random.rand(num_topics) for _ in range(num_clusters)]
    cluster_means = [cluster_length * a / np.linalg.norm(a) for a in cluster_means]
    user_prefs = []
    for _ in range(num_users):
        t = np.random.rand(num_topics)
        user_diff = user_length * t / np.linalg.norm(t) 
        user_prefs.append(cluster_means[np.random.randint(num_clusters)] + user_diff)
    return user_prefs

def user_from_prefs(u):
    i, pref = u
    name = f"user{i}"
    print("Building user", i)
    user = users.User(name, name, name, pref, np.random.randint(35, 60))
    user.into_database()

list(map(user_from_prefs, enumerate(synthetic_user_prefs(100, 10, 25, 55, 30))))


